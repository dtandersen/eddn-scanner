from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SystemState:
    system_id: int
    state: str
    power: Optional[str]
    timestamp: datetime
