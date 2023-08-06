from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Event")


@attr.s(auto_attribs=True)
class Event:
    """
    Attributes:
        name (str):
        start (Union[Unset, None, str]):
        end (Union[Unset, None, str]):
        description (Union[Unset, None, str]):
        definition (Union[Unset, str]):
    """

    name: str
    start: Union[Unset, None, str] = UNSET
    end: Union[Unset, None, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    definition: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        start = self.start
        end = self.end
        description = self.description
        definition = self.definition

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if description is not UNSET:
            field_dict["description"] = description
        if definition is not UNSET:
            field_dict["definition"] = definition

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        start = d.pop("start", UNSET)

        end = d.pop("end", UNSET)

        description = d.pop("description", UNSET)

        definition = d.pop("definition", UNSET)

        event = cls(
            name=name,
            start=start,
            end=end,
            description=description,
            definition=definition,
        )

        event.additional_properties = d
        return event

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
