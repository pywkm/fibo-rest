from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from api.types import FiboSequence


@dataclass
class RequestStatus:
    length: int
    calculated_numbers: int
    requested_at: datetime
    eta: datetime


@dataclass
class SequenceStatusDTO:
    sequence: Optional[FiboSequence] = None
    status: Optional[RequestStatus] = None
