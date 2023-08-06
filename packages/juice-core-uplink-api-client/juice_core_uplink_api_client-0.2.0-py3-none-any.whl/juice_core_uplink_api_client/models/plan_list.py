import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlanList")


@attr.s(auto_attribs=True)
class PlanList:
    """
    Attributes:
        trajectory (str):
        name (str):
        mnemonic (str):
        is_public (bool):
        created (Union[Unset, datetime.datetime]):
        id (Union[Unset, int]):
        author (Union[Unset, str]):
        description (Union[Unset, None, str]):
        refine_log (Union[Unset, str]):
        ptr_file (Union[Unset, str]):
    """

    trajectory: str
    name: str
    mnemonic: str
    is_public: bool
    created: Union[Unset, datetime.datetime] = UNSET
    id: Union[Unset, int] = UNSET
    author: Union[Unset, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    refine_log: Union[Unset, str] = UNSET
    ptr_file: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trajectory = self.trajectory
        name = self.name
        mnemonic = self.mnemonic
        is_public = self.is_public
        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        id = self.id
        author = self.author
        description = self.description
        refine_log = self.refine_log
        ptr_file = self.ptr_file

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trajectory": trajectory,
                "name": name,
                "mnemonic": mnemonic,
                "is_public": is_public,
            }
        )
        if created is not UNSET:
            field_dict["created"] = created
        if id is not UNSET:
            field_dict["id"] = id
        if author is not UNSET:
            field_dict["author"] = author
        if description is not UNSET:
            field_dict["description"] = description
        if refine_log is not UNSET:
            field_dict["refine_log"] = refine_log
        if ptr_file is not UNSET:
            field_dict["ptr_file"] = ptr_file

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trajectory = d.pop("trajectory")

        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        is_public = d.pop("is_public")

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        id = d.pop("id", UNSET)

        author = d.pop("author", UNSET)

        description = d.pop("description", UNSET)

        refine_log = d.pop("refine_log", UNSET)

        ptr_file = d.pop("ptr_file", UNSET)

        plan_list = cls(
            trajectory=trajectory,
            name=name,
            mnemonic=mnemonic,
            is_public=is_public,
            created=created,
            id=id,
            author=author,
            description=description,
            refine_log=refine_log,
            ptr_file=ptr_file,
        )

        plan_list.additional_properties = d
        return plan_list

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
