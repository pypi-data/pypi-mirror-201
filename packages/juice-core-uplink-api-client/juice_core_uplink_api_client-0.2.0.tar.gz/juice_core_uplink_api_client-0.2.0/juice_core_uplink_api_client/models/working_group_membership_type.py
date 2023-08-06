from enum import Enum


class WorkingGroupMembershipType(str, Enum):
    LEADER = "LEADER"
    MEMBER = "MEMBER"

    def __str__(self) -> str:
        return str(self.value)
