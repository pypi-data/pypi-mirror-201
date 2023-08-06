from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DataProfile")


@attr.s(auto_attribs=True)
class DataProfile:
    """
    Attributes:
        event (str):
        time (str):
        mode (str):
        data_rate (Union[Unset, str]):
        comment (Union[Unset, None, str]): Comment when exported to observation definition file
        unit (Union[Unset, str]):
    """

    event: str
    time: str
    mode: str
    data_rate: Union[Unset, str] = UNSET
    comment: Union[Unset, None, str] = UNSET
    unit: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        event = self.event
        time = self.time
        mode = self.mode
        data_rate = self.data_rate
        comment = self.comment
        unit = self.unit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event": event,
                "time": time,
                "mode": mode,
            }
        )
        if data_rate is not UNSET:
            field_dict["data_rate"] = data_rate
        if comment is not UNSET:
            field_dict["comment"] = comment
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        event = d.pop("event")

        time = d.pop("time")

        mode = d.pop("mode")

        data_rate = d.pop("data_rate", UNSET)

        comment = d.pop("comment", UNSET)

        unit = d.pop("unit", UNSET)

        data_profile = cls(
            event=event,
            time=time,
            mode=mode,
            data_rate=data_rate,
            comment=comment,
            unit=unit,
        )

        data_profile.additional_properties = d
        return data_profile

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
