from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReadOnlyInstrumentResourceProfile")


@attr.s(auto_attribs=True)
class ReadOnlyInstrumentResourceProfile:
    """
    Attributes:
        value (float):
        instrument (Union[Unset, str]):
        category (Union[Unset, str]):
        target (Union[Unset, str]):
        unit (Union[Unset, str]):
    """

    value: float
    instrument: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    target: Union[Unset, str] = UNSET
    unit: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        instrument = self.instrument
        category = self.category
        target = self.target
        unit = self.unit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
            }
        )
        if instrument is not UNSET:
            field_dict["instrument"] = instrument
        if category is not UNSET:
            field_dict["category"] = category
        if target is not UNSET:
            field_dict["target"] = target
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        instrument = d.pop("instrument", UNSET)

        category = d.pop("category", UNSET)

        target = d.pop("target", UNSET)

        unit = d.pop("unit", UNSET)

        read_only_instrument_resource_profile = cls(
            value=value,
            instrument=instrument,
            category=category,
            target=target,
            unit=unit,
        )

        read_only_instrument_resource_profile.additional_properties = d
        return read_only_instrument_resource_profile

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
