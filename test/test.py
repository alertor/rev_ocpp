import asyncio
import logging
import websockets
import time

from ocpp.v16 import call, call_result
from ocpp.v16 import ChargePoint as cp

from util import utc_datetime

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):

    async def execute(self):

        await self.send_boot_notification()
        id = await self.send_start_transaction()
        time.sleep(3)
        await self.send_stop_transaction(id)

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model='Model S',
            charge_point_vendor='TravDawg'
        )
        response = await self.call(request)

        if response.status == 'Accepted':
            print("Connected to central system.")

    async def send_auth(self):
        request = call.AuthorizePayload(id_tag='ABC123')
        response = await self.call(request)

        print(response)

    async def send_start_transaction(self) -> int:
        request = call.StartTransactionPayload(
            connector_id=1,
            id_tag='ABC123',
            meter_start=0,
            timestamp=utc_datetime().isoformat()
        )

        response: call_result.StartTransactionPayload = await self.call(request)
        print(response)
        return response.transaction_id

    async def send_stop_transaction(self, id):
        request = call.StopTransactionPayload(
            meter_stop=123,
            timestamp=utc_datetime().isoformat(),
            transaction_id=id,
            id_tag='ABC123'
        )

        response = await self.call(request)
        print(response)


async def main():
    async with websockets.connect(
        'ws://localhost:8000/ocpp/1_6/veefil-12465',
        subprotocols=['ocpp1.6']
    ) as ws:

        cp = ChargePoint('test1', ws)
        await asyncio.gather(cp.start(), cp.execute())
        await ws.close()


if __name__ == '__main__':
   asyncio.run(main())
