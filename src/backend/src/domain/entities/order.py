from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from src.domain.entities import BaseEntity
from src.domain.value_objects import OrderStatus, Skill


@dataclass_json
@dataclass
class Order(BaseEntity):
    uuid: str
    title: str
    description: str
    author_id: str
    status: OrderStatus
    primary_responses: int
    skills: list[Skill] = field(default_factory=list)

    def change_status(self, new_status: OrderStatus):
        if not self.status.can_transition_to(new_status):
            raise ValueError(
                f"It is impossible to change {self.status} to {new_status}"
            )
        self.status = new_status
