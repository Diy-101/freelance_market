from __future__ import annotations

from enum import Enum


class OrderStatus(str, Enum):
    """
    Status for order
    """

    MODERATION = "moderation"
    PUBLISHED = "published"
    NEGOTIATION = "negotiation"
    WORK = "work"
    FINISHED = "finished"

    def can_transition_to(self, new_status: OrderStatus):
        transitions = {
            OrderStatus.MODERATION: [OrderStatus.PUBLISHED],
            OrderStatus.PUBLISHED: [OrderStatus.NEGOTIATION],
            OrderStatus.NEGOTIATION: [OrderStatus.WORK],
            OrderStatus.WORK: [OrderStatus.FINISHED],
            OrderStatus.FINISHED: [],
        }

        return new_status in transitions[self]
