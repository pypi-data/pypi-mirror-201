from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PowerProfile")


@attr.s(auto_attribs=True)
class PowerProfile:
    """
    Attributes:
        event (str):
        time (str):
        mode (str):
        power (Union[Unset, str]):
        comment (Union[Unset, None, str]): Comment when exported to observation definition file
        unit (Union[Unset, str]):
    """

    event: str
    time: str
    mode: str
    power: Union[Unset, str] = UNSET
    comment: Union[Unset, None, str] = UNSET
    unit: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        event = self.event
        time = self.time
        mode = self.mode
        power = self.power
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
        if power is not UNSET:
            field_dict["power"] = power
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

        power = d.pop("power", UNSET)

        comment = d.pop("comment", UNSET)

        unit = d.pop("unit", UNSET)

        power_profile = cls(
            event=event,
            time=time,
            mode=mode,
            power=power,
            comment=comment,
            unit=unit,
        )

        power_profile.additional_properties = d
        return power_profile

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
