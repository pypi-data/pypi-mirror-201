from enum import Enum


class InstrumentMembershipType(str, Enum):
    PI = "PI"
    MEMBER = "MEMBER"

    def __str__(self) -> str:
        return str(self.value)
