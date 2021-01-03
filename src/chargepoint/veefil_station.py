from ocpp.routing import on
from ocpp.v16 import call_result
from ocpp.v16.enums import (
    Action,
    DataTransferStatus
)


from .core import CoreProfile


class VeefillChargePoint(CoreProfile):

    # TODO: Implement custom Veefil data transfer messages
    @on(Action.DataTransfer)
    async def _on_data_transfer(self, vendor_id, message_id, data, **kwargs) -> call_result.DataTransferPayload:
        return call_result.DataTransferPayload(
            status=DataTransferStatus.accepted
        )
