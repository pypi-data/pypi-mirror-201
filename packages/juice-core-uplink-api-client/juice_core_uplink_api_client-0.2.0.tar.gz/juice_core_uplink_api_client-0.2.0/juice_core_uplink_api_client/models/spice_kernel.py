from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="SpiceKernel")


@attr.s(auto_attribs=True)
class SpiceKernel:
    """
    Attributes:
        name (str):
        mnemonic (str):
        path (str):
    """

    name: str
    mnemonic: str
    path: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        mnemonic = self.mnemonic
        path = self.path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
                "path": path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        path = d.pop("path")

        spice_kernel = cls(
            name=name,
            mnemonic=mnemonic,
            path=path,
        )

        spice_kernel.additional_properties = d
        return spice_kernel

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
