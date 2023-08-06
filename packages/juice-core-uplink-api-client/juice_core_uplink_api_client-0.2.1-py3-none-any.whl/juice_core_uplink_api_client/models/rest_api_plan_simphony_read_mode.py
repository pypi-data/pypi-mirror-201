from enum import Enum


class RestApiPlanSimphonyReadMode(str, Enum):
    STRICT = "strict"
    OPEN = "open"

    def __str__(self) -> str:
        return str(self.value)
