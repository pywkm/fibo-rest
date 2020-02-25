from dataclasses import dataclass
from datetime import datetime


@dataclass
class RequestStatus:
    length: int
    calculated_items: int
    requested_at: datetime
    eta: datetime
