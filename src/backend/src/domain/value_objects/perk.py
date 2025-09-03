from dataclasses import dataclass


@dataclass
class Perk:
    name: str
    icon: str | None = None
