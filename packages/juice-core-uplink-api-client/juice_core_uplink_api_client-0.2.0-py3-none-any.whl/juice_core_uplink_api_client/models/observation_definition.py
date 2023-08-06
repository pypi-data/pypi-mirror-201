from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_profile import DataProfile
    from ..models.power_profile import PowerProfile


T = TypeVar("T", bound="ObservationDefinition")


@attr.s(auto_attribs=True)
class ObservationDefinition:
    """
    Attributes:
        name (str):
        mnemonic (str):
        payload (str):
        pointing_type (str):
        target (str):
        segment_definitions (List[str]):
        id (Union[Unset, int]):
        description (Union[Unset, None, str]):
        data_profile (Union[Unset, None, List['DataProfile']]):
        power_profile (Union[Unset, None, List['PowerProfile']]):
        ptr_snippet_file (Union[Unset, None, str]):
        itl_snippet_file (Union[Unset, None, str]):
        ptr_snippet (Union[Unset, None, str]):
        itl_snippet (Union[Unset, None, str]):
    """

    name: str
    mnemonic: str
    payload: str
    pointing_type: str
    target: str
    segment_definitions: List[str]
    id: Union[Unset, int] = UNSET
    description: Union[Unset, None, str] = UNSET
    data_profile: Union[Unset, None, List["DataProfile"]] = UNSET
    power_profile: Union[Unset, None, List["PowerProfile"]] = UNSET
    ptr_snippet_file: Union[Unset, None, str] = UNSET
    itl_snippet_file: Union[Unset, None, str] = UNSET
    ptr_snippet: Union[Unset, None, str] = UNSET
    itl_snippet: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        mnemonic = self.mnemonic
        payload = self.payload
        pointing_type = self.pointing_type
        target = self.target
        segment_definitions = self.segment_definitions

        id = self.id
        description = self.description
        data_profile: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.data_profile, Unset):
            if self.data_profile is None:
                data_profile = None
            else:
                data_profile = []
                for data_profile_item_data in self.data_profile:
                    data_profile_item = data_profile_item_data.to_dict()

                    data_profile.append(data_profile_item)

        power_profile: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.power_profile, Unset):
            if self.power_profile is None:
                power_profile = None
            else:
                power_profile = []
                for power_profile_item_data in self.power_profile:
                    power_profile_item = power_profile_item_data.to_dict()

                    power_profile.append(power_profile_item)

        ptr_snippet_file = self.ptr_snippet_file
        itl_snippet_file = self.itl_snippet_file
        ptr_snippet = self.ptr_snippet
        itl_snippet = self.itl_snippet

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
                "payload": payload,
                "pointing_type": pointing_type,
                "target": target,
                "segment_definitions": segment_definitions,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if description is not UNSET:
            field_dict["description"] = description
        if data_profile is not UNSET:
            field_dict["data_profile"] = data_profile
        if power_profile is not UNSET:
            field_dict["power_profile"] = power_profile
        if ptr_snippet_file is not UNSET:
            field_dict["PTRSnippet_file"] = ptr_snippet_file
        if itl_snippet_file is not UNSET:
            field_dict["ITLSnippet_file"] = itl_snippet_file
        if ptr_snippet is not UNSET:
            field_dict["PTRSnippet"] = ptr_snippet
        if itl_snippet is not UNSET:
            field_dict["ITLSnippet"] = itl_snippet

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.data_profile import DataProfile
        from ..models.power_profile import PowerProfile

        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        payload = d.pop("payload")

        pointing_type = d.pop("pointing_type")

        target = d.pop("target")

        segment_definitions = cast(List[str], d.pop("segment_definitions"))

        id = d.pop("id", UNSET)

        description = d.pop("description", UNSET)

        data_profile = []
        _data_profile = d.pop("data_profile", UNSET)
        for data_profile_item_data in _data_profile or []:
            data_profile_item = DataProfile.from_dict(data_profile_item_data)

            data_profile.append(data_profile_item)

        power_profile = []
        _power_profile = d.pop("power_profile", UNSET)
        for power_profile_item_data in _power_profile or []:
            power_profile_item = PowerProfile.from_dict(power_profile_item_data)

            power_profile.append(power_profile_item)

        ptr_snippet_file = d.pop("PTRSnippet_file", UNSET)

        itl_snippet_file = d.pop("ITLSnippet_file", UNSET)

        ptr_snippet = d.pop("PTRSnippet", UNSET)

        itl_snippet = d.pop("ITLSnippet", UNSET)

        observation_definition = cls(
            name=name,
            mnemonic=mnemonic,
            payload=payload,
            pointing_type=pointing_type,
            target=target,
            segment_definitions=segment_definitions,
            id=id,
            description=description,
            data_profile=data_profile,
            power_profile=power_profile,
            ptr_snippet_file=ptr_snippet_file,
            itl_snippet_file=itl_snippet_file,
            ptr_snippet=ptr_snippet,
            itl_snippet=itl_snippet,
        )

        observation_definition.additional_properties = d
        return observation_definition

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
