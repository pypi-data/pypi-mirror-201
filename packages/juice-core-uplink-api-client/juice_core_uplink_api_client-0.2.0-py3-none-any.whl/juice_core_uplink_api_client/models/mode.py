from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Mode")


@attr.s(auto_attribs=True)
class Mode:
    """
    Attributes:
        name (str):
        mnemonic (str):
        payload (str):
        description (Union[Unset, None, str]):
        mapps_mode (Union[Unset, None, str]):
        power (Union[Unset, None, float]):
        data_rate (Union[Unset, None, float]):
        inactive (Union[Unset, bool]):
        comments (Union[Unset, None, str]):
    """

    name: str
    mnemonic: str
    payload: str
    description: Union[Unset, None, str] = UNSET
    mapps_mode: Union[Unset, None, str] = UNSET
    power: Union[Unset, None, float] = UNSET
    data_rate: Union[Unset, None, float] = UNSET
    inactive: Union[Unset, bool] = UNSET
    comments: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        mnemonic = self.mnemonic
        payload = self.payload
        description = self.description
        mapps_mode = self.mapps_mode
        power = self.power
        data_rate = self.data_rate
        inactive = self.inactive
        comments = self.comments

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
                "payload": payload,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if mapps_mode is not UNSET:
            field_dict["mapps_mode"] = mapps_mode
        if power is not UNSET:
            field_dict["power"] = power
        if data_rate is not UNSET:
            field_dict["data_rate"] = data_rate
        if inactive is not UNSET:
            field_dict["inactive"] = inactive
        if comments is not UNSET:
            field_dict["comments"] = comments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        payload = d.pop("payload")

        description = d.pop("description", UNSET)

        mapps_mode = d.pop("mapps_mode", UNSET)

        power = d.pop("power", UNSET)

        data_rate = d.pop("data_rate", UNSET)

        inactive = d.pop("inactive", UNSET)

        comments = d.pop("comments", UNSET)

        mode = cls(
            name=name,
            mnemonic=mnemonic,
            payload=payload,
            description=description,
            mapps_mode=mapps_mode,
            power=power,
            data_rate=data_rate,
            inactive=inactive,
            comments=comments,
        )

        mode.additional_properties = d
        return mode

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
