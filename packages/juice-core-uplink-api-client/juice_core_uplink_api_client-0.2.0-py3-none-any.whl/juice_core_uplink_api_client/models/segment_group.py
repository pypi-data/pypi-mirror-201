from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.instrument_resource_profile import InstrumentResourceProfile
    from ..models.resource_profile import ResourceProfile


T = TypeVar("T", bound="SegmentGroup")


@attr.s(auto_attribs=True)
class SegmentGroup:
    """
    Attributes:
        name (str):
        mnemonic (str):
        resources (Union[Unset, None, List['ResourceProfile']]):
        instrument_resources (Union[Unset, None, List['InstrumentResourceProfile']]):
        platform_power_profile (Union[Unset, None, str]):
    """

    name: str
    mnemonic: str
    resources: Union[Unset, None, List["ResourceProfile"]] = UNSET
    instrument_resources: Union[Unset, None, List["InstrumentResourceProfile"]] = UNSET
    platform_power_profile: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        mnemonic = self.mnemonic
        resources: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.resources, Unset):
            if self.resources is None:
                resources = None
            else:
                resources = []
                for resources_item_data in self.resources:
                    resources_item = resources_item_data.to_dict()

                    resources.append(resources_item)

        instrument_resources: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.instrument_resources, Unset):
            if self.instrument_resources is None:
                instrument_resources = None
            else:
                instrument_resources = []
                for instrument_resources_item_data in self.instrument_resources:
                    instrument_resources_item = instrument_resources_item_data.to_dict()

                    instrument_resources.append(instrument_resources_item)

        platform_power_profile = self.platform_power_profile

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
            }
        )
        if resources is not UNSET:
            field_dict["resources"] = resources
        if instrument_resources is not UNSET:
            field_dict["instrument_resources"] = instrument_resources
        if platform_power_profile is not UNSET:
            field_dict["platform_power_profile"] = platform_power_profile

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.instrument_resource_profile import InstrumentResourceProfile
        from ..models.resource_profile import ResourceProfile

        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        resources = []
        _resources = d.pop("resources", UNSET)
        for resources_item_data in _resources or []:
            resources_item = ResourceProfile.from_dict(resources_item_data)

            resources.append(resources_item)

        instrument_resources = []
        _instrument_resources = d.pop("instrument_resources", UNSET)
        for instrument_resources_item_data in _instrument_resources or []:
            instrument_resources_item = InstrumentResourceProfile.from_dict(instrument_resources_item_data)

            instrument_resources.append(instrument_resources_item)

        platform_power_profile = d.pop("platform_power_profile", UNSET)

        segment_group = cls(
            name=name,
            mnemonic=mnemonic,
            resources=resources,
            instrument_resources=instrument_resources,
            platform_power_profile=platform_power_profile,
        )

        segment_group.additional_properties = d
        return segment_group

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
