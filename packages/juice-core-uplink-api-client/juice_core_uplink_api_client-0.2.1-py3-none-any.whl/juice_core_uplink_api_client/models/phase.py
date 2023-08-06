import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Phase")


@attr.s(auto_attribs=True)
class Phase:
    """
    Attributes:
        name (str):
        mnemonic (str):
        start (Union[Unset, None, datetime.datetime]):
        end (Union[Unset, None, datetime.datetime]):
    """

    name: str
    mnemonic: str
    start: Union[Unset, None, datetime.datetime] = UNSET
    end: Union[Unset, None, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        mnemonic = self.mnemonic
        start: Union[Unset, None, str] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.isoformat() if self.start else None

        end: Union[Unset, None, str] = UNSET
        if not isinstance(self.end, Unset):
            end = self.end.isoformat() if self.end else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
            }
        )
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        _start = d.pop("start", UNSET)
        start: Union[Unset, None, datetime.datetime]
        if _start is None:
            start = None
        elif isinstance(_start, Unset):
            start = UNSET
        else:
            start = isoparse(_start)

        _end = d.pop("end", UNSET)
        end: Union[Unset, None, datetime.datetime]
        if _end is None:
            end = None
        elif isinstance(_end, Unset):
            end = UNSET
        else:
            end = isoparse(_end)

        phase = cls(
            name=name,
            mnemonic=mnemonic,
            start=start,
            end=end,
        )

        phase.additional_properties = d
        return phase

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
