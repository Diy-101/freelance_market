from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    icon: str | None = None
