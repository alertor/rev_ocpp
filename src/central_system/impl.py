from typing import Dict, List, Union

from ocpp.v16 import ChargePoint


class CentralSystem(object):

    _chargepoint_ids: List[str]
    _chargepoints: Dict[str, ChargePoint]

    def __init__(self):
        self._chargepoint_ids = []
        self._chargepoints = {}

    def register_chargepoint(self, cp: ChargePoint):
        if cp.id not in self._chargepoint_ids:
            self._chargepoint_ids.append(cp.id)
        self._chargepoints[cp.id] = cp

    def deregister_chargepoint(self, cp: Union[str, ChargePoint]) -> bool:
        identity = cp.id if isinstance(cp, ChargePoint) else cp
        try:
            self._chargepoint_ids.remove(identity)
            self._chargepoints.pop(identity)
            return True
        except (ValueError, KeyError):
            return False

    def get_chargepoint(self, identity: str) -> ChargePoint:
        return self._chargepoints[identity]

    @property
    def chargepoints(self):
        return self._chargepoint_ids
