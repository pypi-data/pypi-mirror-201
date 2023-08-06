from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SeriesDefinition")


@attr.s(auto_attribs=True)
class SeriesDefinition:
    """
    Attributes:
        name (str):
        mnemonic (str):
        unit (Union[Unset, None, str]):
        category (Union[Unset, str]):
        description (Union[Unset, None, str]):
    """

    name: str
    mnemonic: str
    unit: Union[Unset, None, str] = UNSET
    category: Union[Unset, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        mnemonic = self.mnemonic
        unit = self.unit
        category = self.category
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
            }
        )
        if unit is not UNSET:
            field_dict["unit"] = unit
        if category is not UNSET:
            field_dict["category"] = category
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        unit = d.pop("unit", UNSET)

        category = d.pop("category", UNSET)

        description = d.pop("description", UNSET)

        series_definition = cls(
            name=name,
            mnemonic=mnemonic,
            unit=unit,
            category=category,
            description=description,
        )

        series_definition.additional_properties = d
        return series_definition

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
