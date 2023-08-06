from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.instrument_membership import InstrumentMembership
    from ..models.working_group_membership import WorkingGroupMembership


T = TypeVar("T", bound="User")


@attr.s(auto_attribs=True)
class User:
    """
    Attributes:
        working_groups (List['WorkingGroupMembership']):
        instruments (List['InstrumentMembership']):
        username (Union[Unset, str]):
        email (Union[Unset, str]):
        first_name (Union[Unset, str]):
        last_name (Union[Unset, str]):
        role (Union[Unset, str]):
    """

    working_groups: List["WorkingGroupMembership"]
    instruments: List["InstrumentMembership"]
    username: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    role: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        working_groups = []
        for working_groups_item_data in self.working_groups:
            working_groups_item = working_groups_item_data.to_dict()

            working_groups.append(working_groups_item)

        instruments = []
        for instruments_item_data in self.instruments:
            instruments_item = instruments_item_data.to_dict()

            instruments.append(instruments_item)

        username = self.username
        email = self.email
        first_name = self.first_name
        last_name = self.last_name
        role = self.role

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "working_groups": working_groups,
                "instruments": instruments,
            }
        )
        if username is not UNSET:
            field_dict["username"] = username
        if email is not UNSET:
            field_dict["email"] = email
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.instrument_membership import InstrumentMembership
        from ..models.working_group_membership import WorkingGroupMembership

        d = src_dict.copy()
        working_groups = []
        _working_groups = d.pop("working_groups")
        for working_groups_item_data in _working_groups:
            working_groups_item = WorkingGroupMembership.from_dict(working_groups_item_data)

            working_groups.append(working_groups_item)

        instruments = []
        _instruments = d.pop("instruments")
        for instruments_item_data in _instruments:
            instruments_item = InstrumentMembership.from_dict(instruments_item_data)

            instruments.append(instruments_item)

        username = d.pop("username", UNSET)

        email = d.pop("email", UNSET)

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        role = d.pop("role", UNSET)

        user = cls(
            working_groups=working_groups,
            instruments=instruments,
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )

        user.additional_properties = d
        return user

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
