from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.read_only_instrument_resource_profile import ReadOnlyInstrumentResourceProfile
    from ..models.read_only_resource_profile import ReadOnlyResourceProfile


T = TypeVar("T", bound="ReadOnlySegmentGroup")


@attr.s(auto_attribs=True)
class ReadOnlySegmentGroup:
    """
    Attributes:
        name (str):
        mnemonic (str):
        resources (List['ReadOnlyResourceProfile']):
        instrument_resources (List['ReadOnlyInstrumentResourceProfile']):
        platform_power_profile (Union[Unset, int]):
    """

    name: str
    mnemonic: str
    resources: List["ReadOnlyResourceProfile"]
    instrument_resources: List["ReadOnlyInstrumentResourceProfile"]
    platform_power_profile: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        mnemonic = self.mnemonic
        resources = []
        for resources_item_data in self.resources:
            resources_item = resources_item_data.to_dict()

            resources.append(resources_item)

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
                "resources": resources,
                "instrument_resources": instrument_resources,
            }
        )
        if platform_power_profile is not UNSET:
            field_dict["platform_power_profile"] = platform_power_profile

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.read_only_instrument_resource_profile import ReadOnlyInstrumentResourceProfile
        from ..models.read_only_resource_profile import ReadOnlyResourceProfile

        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        resources = []
        _resources = d.pop("resources")
        for resources_item_data in _resources:
            resources_item = ReadOnlyResourceProfile.from_dict(resources_item_data)

            resources.append(resources_item)

        instrument_resources = []
        _instrument_resources = d.pop("instrument_resources")
        for instrument_resources_item_data in _instrument_resources:
            instrument_resources_item = ReadOnlyInstrumentResourceProfile.from_dict(instrument_resources_item_data)

            instrument_resources.append(instrument_resources_item)

        platform_power_profile = d.pop("platform_power_profile", UNSET)

        read_only_segment_group = cls(
            name=name,
            mnemonic=mnemonic,
            resources=resources,
            instrument_resources=instrument_resources,
            platform_power_profile=platform_power_profile,
        )

        read_only_segment_group.additional_properties = d
        return read_only_segment_group

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
