from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="InstrumentType")


@attr.s(auto_attribs=True)
class InstrumentType:
    """
    Attributes:
        name (str):
        mnemonic (str):
        instrument_set (Union[Unset, List[str]]):
    """

    name: str
    mnemonic: str
    instrument_set: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        mnemonic = self.mnemonic
        instrument_set: Union[Unset, List[str]] = UNSET
        if not isinstance(self.instrument_set, Unset):
            instrument_set = self.instrument_set

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
            }
        )
        if instrument_set is not UNSET:
            field_dict["instrument_set"] = instrument_set

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        instrument_set = cast(List[str], d.pop("instrument_set", UNSET))

        instrument_type = cls(
            name=name,
            mnemonic=mnemonic,
            instrument_set=instrument_set,
        )

        instrument_type.additional_properties = d
        return instrument_type

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
