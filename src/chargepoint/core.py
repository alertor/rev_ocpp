from dateutil import parser
from json import dumps
from typing import Dict, List, Optional

from ocpp.routing import on
from ocpp.v16 import call, call_result, ChargePoint as BaseChargePoint
from ocpp.v16.enums import (
    Action,
    AvailabilityType,
    AuthorizationStatus,
    ChargePointErrorCode,
    ChargePointStatus,
    RegistrationStatus,
    ResetType
)

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from util import utc_datetime

from db.mongo.log import log_message
from db.models import (
    AuthorizationRequest,
    ChargePoint,
    ChargePointError,
    Connector,
    InProgressTransaction,
    Token,
    Transaction,
)

from network.websocket_adaptor import FastAPIWebSocketAdaptor

from .exceptions import ChargePointNotAuthorized
from .types import MeterValue


class CoreProfile(BaseChargePoint):
    """
    Abstract class implementing the Core Profile of the OCPP1.6 spec. Requires the concrete class to implement all
    request handlers.
    """

    def __init__(
            self,
            charge_point_id: str,
            websocket: FastAPIWebSocketAdaptor,
            session: Session
    ):
        super(CoreProfile, self).__init__(charge_point_id, websocket)
        self._session = session
        self._in_progress_transactions = Dict[int, InProgressTransaction]

        self._data_object = self._authenticate_charge_point(charge_point_id)

    async def _handle_call(self, msg):
        await super(CoreProfile, self)._handle_call(msg)
        # Log the raw message to mongo for debugging
        log_message({
            'action': msg.action,
            'payload': msg.payload
        }, self._data_object.identity)

    def _authenticate_charge_point(self, charge_point_id) -> ChargePoint:
        try:
            return self._session.query(ChargePoint).filter(ChargePoint.identity == charge_point_id).one()
        except NoResultFound:
            raise ChargePointNotAuthorized

    def _get_token(self, id_tag) -> Optional[Token]:
        try:
            return self._session.query(Token).filter(Token.token == id_tag).one()
        except (MultipleResultsFound, NoResultFound):
            return None

    def _get_connector(self, connector_id) -> Optional[Connector]:
        return next((c for c in self._data_object.connectors if c.connector_id == connector_id), None)

    # Incoming requests
    @on(Action.Authorize)
    async def _on_authorize(self, id_tag: str, **kwargs) -> call_result.AuthorizePayload:
        # Generate auth request without known token id - will be determined by the db query
        authorized = AuthorizationStatus.blocked
        auth_req = AuthorizationRequest(
            token_string=id_tag,
            chargepoint=self._data_object,
            timestamp=utc_datetime()
        )

        try:
            auth_req.token = self._session.query(Token).filter(Token.token == id_tag).one()
            authorized = AuthorizationStatus.accepted
        except (MultipleResultsFound, NoResultFound):
            pass

        self._session.add(auth_req)
        self._session.commit()

        # TODO: Add parent tag if exists
        return call_result.AuthorizePayload(
            id_tag_info={
                'status': authorized
            }
        )

    # TODO: Any use for model/vendor/other info?
    @on(Action.BootNotification)
    async def _on_boot_notification(
            self,
            charge_point_vendor,
            charge_point_model,
            **kwargs) -> call_result.BootNotificationPayload:
        self._data_object.boot_timestamp = utc_datetime()
        self._session.commit()

        return call_result.BootNotificationPayload(
            current_time=utc_datetime().isoformat(),
            interval=5,
            status=RegistrationStatus.accepted
        )

    @on(Action.DataTransfer)
    async def _on_data_transfer(self, vendor_id, message_id, data, **kwargs) -> call_result.DataTransferPayload:
        raise NotImplementedError

    @on(Action.Heartbeat)
    async def _on_heartbeat(self, **kwargs) -> call_result.HeartbeatPayload:
        self._data_object.last_heartbeat = utc_datetime()
        self._session.commit()

        return call_result.HeartbeatPayload(
            current_time=utc_datetime().isoformat()
        )

    # TODO meter values
    @on(Action.MeterValues)
    async def _on_meter_values(
            self,
            connector_id: int,
            transaction_id: int,
            meter_value: List[MeterValue],
            **kwargs) -> call_result.MeterValuesPayload:
        return call_result.MeterValuesPayload()

    @on(Action.StartTransaction)
    async def _on_start_transaction(
            self,
            connector_id: int,
            id_tag: str,
            meter_start: int,
            timestamp: str,
            reservation_id: int = None,
            **kwargs) -> call_result.StartTransactionPayload:
        # Get data objects
        token = self._get_token(id_tag)
        connector = next(c for c in self._data_object.connectors if c.id == connector_id)

        # Set up the in progress transaction
        transaction = InProgressTransaction(
            start_timestamp=parser.parse(timestamp),
            meter_start=meter_start,
            reservation_id=reservation_id,
            start_token=token,
            connector=connector
        )
        self._session.add(transaction)
        self._session.commit()

        return call_result.StartTransactionPayload(
            transaction_id=transaction.id,
            id_tag_info={
                'status': AuthorizationStatus.accepted
            }
        )

    @on(Action.StatusNotification)
    async def _on_status_notification(
            self,
            connector_id: int,
            error_code: ChargePointErrorCode,
            status: ChargePointStatus,
            timestamp: str = None,
            info: str = None,
            vendor_id: str = None,
            vendor_error_code: str = None,
            **kwargs) -> call_result.StatusNotificationPayload:
        # Get the connector object this notification references
        connector = self._get_connector(connector_id)

        # Generate the database object
        err = ChargePointError(
            connector=connector,
            error_code=error_code.value,
            status=status.value,
            timestamp=timestamp if timestamp else utc_datetime(),
            info=info,
            vendor_id=vendor_id,
            vendor_error_code=vendor_error_code
        )

        self._session.add(err)
        self._session.commit()

        return call_result.StatusNotificationPayload()

    @on(Action.StopTransaction)
    async def _on_stop_transaction(
            self,
            meter_stop: int,
            timestamp: str,
            transaction_id: int,
            reason: str = None,
            id_tag: str = None,
            transaction_data: List = None,
            **kwargs) -> call_result.StopTransactionPayload:
        token = self._get_token(id_tag)
        try:
            progress_transaction: InProgressTransaction = self._session.query(InProgressTransaction) \
                .filter(InProgressTransaction.id == transaction_id).one()
        except (NoResultFound, MultipleResultsFound):
            print(f"Failed to complete a transaction with id: {transaction_id}-"
                  f" no matching transaction found in database")
            return call_result.StopTransactionPayload(
                id_tag_info=None
            )

        # Construct the complete transaction
        end_time = parser.parse(timestamp)
        transaction = Transaction(
            reservation_id=progress_transaction.reservation_id,
            start_timestamp=progress_transaction.start_timestamp,
            end_timestamp=end_time,
            duration=end_time - progress_transaction.start_timestamp,
            meter_start=progress_transaction.meter_start,
            meter_stop=meter_stop,
            meter_used=meter_stop-progress_transaction.meter_start,
            stop_reason=reason,
            connector=progress_transaction.connector,
            end_token=token,
            start_token=progress_transaction.start_token
        )

        self._session.add(transaction)
        self._session.delete(progress_transaction)
        self._session.commit()

        return call_result.StopTransactionPayload(
            id_tag_info={
                'status': AuthorizationStatus.accepted
            }
        )

    async def send_change_availability(self, connector_id: int, availability_type: AvailabilityType) -> call_result.ChangeAvailabilityPayload:
        return await self.call(
            call.ChangeAvailabilityPayload(
                connector_id=connector_id,
                type=availability_type
            )
        )

    async def send_change_configuration(self, key: str, value: str) -> call_result.ChangeConfigurationPayload:
        return await self.call(
            call.ChangeConfigurationPayload(
                key=key,
                value=value
            )
        )

    async def send_clear_cache(self) -> call_result.ClearCachePayload:
        return await self.call(call.ClearCachePayload())

    async def send_data_transfer(self, vendor_id: str, message_id: str = None, data: str = None) -> call_result.DataTransferPayload:
        return await self.call(
            call.DataTransferPayload(
                vendor_id=vendor_id,
                message_id=message_id,
                data=data
            )
        )

    async def send_get_configuration(self, key: List[str] = None) -> call_result.GetConfigurationPayload:
        return await self.call(
            call.GetConfigurationPayload(key=key)
        )

    async def send_remote_start_transaction(self, id_tag: str, connector_id: int = None, charging_profile: Dict = None) -> call_result.RemoteStartTransactionPayload:
        return await self.call(
            call.RemoteStartTransactionPayload(
                id_tag=id_tag,
                connector_id=connector_id,
                charging_profile=charging_profile
            )
        )

    async def send_remote_stop_transaction(self, transaction_id: int) -> call_result.RemoteStopTransactionPayload:
        return await self.call(
            call.RemoteStopTransactionPayload(transaction_id=transaction_id)
        )

    async def send_reset(self, type: ResetType) -> call_result.ResetPayload:
        return await self.call(
            call.ResetPayload(type=type)
        )

    async def send_unlock_connector(self, connector_id: int) -> call_result.UnlockConnectorPayload:
        return await self.call(
            call.UnlockConnectorPayload(connector_id=connector_id)
        )
