from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Event:
    timestamp: datetime
    user: str
    source: str
    event_type: str
    target: str
    outcome: str

    device_id: Optional[str] = None
    ip_address: Optional[str] = None

    metadata: dict = field(default_factory=dict)