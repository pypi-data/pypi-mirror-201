from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="InstrumentResourceProfile")


@attr.s(auto_attribs=True)
class InstrumentResourceProfile:
    """
    Attributes:
        category (str):
        target (str):
        unit (str):
        instrument (str):
        value (Union[Unset, None, float]):
    """

    category: str
    target: str
    unit: str
    instrument: str
    value: Union[Unset, None, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        category = self.category
        target = self.target
        unit = self.unit
        instrument = self.instrument
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "category": category,
                "target": target,
                "unit": unit,
                "instrument": instrument,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        category = d.pop("category")

        target = d.pop("target")

        unit = d.pop("unit")

        instrument = d.pop("instrument")

        value = d.pop("value", UNSET)

        instrument_resource_profile = cls(
            category=category,
            target=target,
            unit=unit,
            instrument=instrument,
            value=value,
        )

        instrument_resource_profile.additional_properties = d
        return instrument_resource_profile

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
