from dataclasses import dataclass
from typing import List, Optional

from ocpp.v16.enums import (
    Measurand,
    Phase,
    ReadingContext,
    ValueFormat,
    Location,
    UnitOfMeasure
)


@dataclass
class SampledValue(object):

    value: str
    context: Optional[ReadingContext]
    format: ValueFormat = ValueFormat.raw
    measurand: Measurand = Measurand.energy_active_import_register
    phase: Phase = Phase.n
    location: Location = Location.outlet
    unit: UnitOfMeasure = UnitOfMeasure.wh


@dataclass
class MeterValue(object):

    timestamp: str
    sampled_value = List[SampledValue]
