from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EngineeringSegmentType")


@attr.s(auto_attribs=True)
class EngineeringSegmentType:
    """
    Attributes:
        mnemonic (str):
        name (str):
        description (Union[Unset, None, str]):
        power (Union[Unset, None, float]):
    """

    mnemonic: str
    name: str
    description: Union[Unset, None, str] = UNSET
    power: Union[Unset, None, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mnemonic = self.mnemonic
        name = self.name
        description = self.description
        power = self.power

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mnemonic": mnemonic,
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if power is not UNSET:
            field_dict["power"] = power

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        mnemonic = d.pop("mnemonic")

        name = d.pop("name")

        description = d.pop("description", UNSET)

        power = d.pop("power", UNSET)

        engineering_segment_type = cls(
            mnemonic=mnemonic,
            name=name,
            description=description,
            power=power,
        )

        engineering_segment_type.additional_properties = d
        return engineering_segment_type

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
