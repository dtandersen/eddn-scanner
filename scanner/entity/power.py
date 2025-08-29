from dataclasses import dataclass


@dataclass
class Power:
    system_address: int
    name: str
    progress: float
