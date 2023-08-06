from enum import Enum


class RestApiPlanSimphonyOppsReadMode(str, Enum):
    STRICT = "strict"
    OPEN = "open"

    def __str__(self) -> str:
        return str(self.value)
