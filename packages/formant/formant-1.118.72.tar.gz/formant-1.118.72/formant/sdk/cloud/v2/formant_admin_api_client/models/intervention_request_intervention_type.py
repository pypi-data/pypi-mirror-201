from enum import Enum


class InterventionRequestInterventionType(str, Enum):
    SELECTION = "selection"
    LABELING = "labeling"
    TELEOP = "teleop"

    def __str__(self) -> str:
        return str(self.value)
