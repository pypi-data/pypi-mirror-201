from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SeriesData")


@attr.s(auto_attribs=True)
class SeriesData:
    """
    Attributes:
        epoch (Union[Unset, None, str]):
        value (Union[Unset, None, float]):
    """

    epoch: Union[Unset, None, str] = UNSET
    value: Union[Unset, None, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        epoch = self.epoch
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if epoch is not UNSET:
            field_dict["epoch"] = epoch
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        epoch = d.pop("epoch", UNSET)

        value = d.pop("value", UNSET)

        series_data = cls(
            epoch=epoch,
            value=value,
        )

        series_data.additional_properties = d
        return series_data

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
