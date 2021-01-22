from typing import Dict, List

from ocpp.v16 import ChargePoint


class CentralSystem(object):

    _chargepoint_ids: List[str]
    _chargepoints: Dict[str, ChargePoint]

    def register_chargepoint(self, cp: ChargePoint):
        self._chargepoint_ids.append(cp.id)
        self._chargepoints[cp.id] = cp

    def get_chargepoint(self, identity: str) -> ChargePoint:
        return self._chargepoints[identity]
