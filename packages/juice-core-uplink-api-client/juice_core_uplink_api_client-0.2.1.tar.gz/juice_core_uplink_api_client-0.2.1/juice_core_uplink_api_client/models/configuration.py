from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.configuration_item import ConfigurationItem
    from ..models.instrument_type import InstrumentType
    from ..models.platform_power_profile import PlatformPowerProfile
    from ..models.resource_category import ResourceCategory
    from ..models.unit import Unit


T = TypeVar("T", bound="Configuration")


@attr.s(auto_attribs=True)
class Configuration:
    """
    Attributes:
        version (str):
        targets (Union[Unset, List['ConfigurationItem']]):
        instruments (Union[Unset, List['ConfigurationItem']]):
        units (Union[Unset, List['Unit']]):
        instrument_types (Union[Unset, List['InstrumentType']]):
        resource_categories (Union[Unset, List['ResourceCategory']]):
        slew_policies (Union[Unset, List['ConfigurationItem']]):
        timelines (Union[Unset, List['ConfigurationItem']]):
        platform_power_profiles (Union[Unset, List['PlatformPowerProfile']]):
    """

    version: str
    targets: Union[Unset, List["ConfigurationItem"]] = UNSET
    instruments: Union[Unset, List["ConfigurationItem"]] = UNSET
    units: Union[Unset, List["Unit"]] = UNSET
    instrument_types: Union[Unset, List["InstrumentType"]] = UNSET
    resource_categories: Union[Unset, List["ResourceCategory"]] = UNSET
    slew_policies: Union[Unset, List["ConfigurationItem"]] = UNSET
    timelines: Union[Unset, List["ConfigurationItem"]] = UNSET
    platform_power_profiles: Union[Unset, List["PlatformPowerProfile"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        version = self.version
        targets: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.targets, Unset):
            targets = []
            for targets_item_data in self.targets:
                targets_item = targets_item_data.to_dict()

                targets.append(targets_item)

        instruments: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.instruments, Unset):
            instruments = []
            for instruments_item_data in self.instruments:
                instruments_item = instruments_item_data.to_dict()

                instruments.append(instruments_item)

        units: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.units, Unset):
            units = []
            for units_item_data in self.units:
                units_item = units_item_data.to_dict()

                units.append(units_item)

        instrument_types: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.instrument_types, Unset):
            instrument_types = []
            for instrument_types_item_data in self.instrument_types:
                instrument_types_item = instrument_types_item_data.to_dict()

                instrument_types.append(instrument_types_item)

        resource_categories: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.resource_categories, Unset):
            resource_categories = []
            for resource_categories_item_data in self.resource_categories:
                resource_categories_item = resource_categories_item_data.to_dict()

                resource_categories.append(resource_categories_item)

        slew_policies: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.slew_policies, Unset):
            slew_policies = []
            for slew_policies_item_data in self.slew_policies:
                slew_policies_item = slew_policies_item_data.to_dict()

                slew_policies.append(slew_policies_item)

        timelines: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.timelines, Unset):
            timelines = []
            for timelines_item_data in self.timelines:
                timelines_item = timelines_item_data.to_dict()

                timelines.append(timelines_item)

        platform_power_profiles: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.platform_power_profiles, Unset):
            platform_power_profiles = []
            for platform_power_profiles_item_data in self.platform_power_profiles:
                platform_power_profiles_item = platform_power_profiles_item_data.to_dict()

                platform_power_profiles.append(platform_power_profiles_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
            }
        )
        if targets is not UNSET:
            field_dict["targets"] = targets
        if instruments is not UNSET:
            field_dict["instruments"] = instruments
        if units is not UNSET:
            field_dict["units"] = units
        if instrument_types is not UNSET:
            field_dict["instrument_types"] = instrument_types
        if resource_categories is not UNSET:
            field_dict["resource_categories"] = resource_categories
        if slew_policies is not UNSET:
            field_dict["slew_policies"] = slew_policies
        if timelines is not UNSET:
            field_dict["timelines"] = timelines
        if platform_power_profiles is not UNSET:
            field_dict["platform_power_profiles"] = platform_power_profiles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.configuration_item import ConfigurationItem
        from ..models.instrument_type import InstrumentType
        from ..models.platform_power_profile import PlatformPowerProfile
        from ..models.resource_category import ResourceCategory
        from ..models.unit import Unit

        d = src_dict.copy()
        version = d.pop("version")

        targets = []
        _targets = d.pop("targets", UNSET)
        for targets_item_data in _targets or []:
            targets_item = ConfigurationItem.from_dict(targets_item_data)

            targets.append(targets_item)

        instruments = []
        _instruments = d.pop("instruments", UNSET)
        for instruments_item_data in _instruments or []:
            instruments_item = ConfigurationItem.from_dict(instruments_item_data)

            instruments.append(instruments_item)

        units = []
        _units = d.pop("units", UNSET)
        for units_item_data in _units or []:
            units_item = Unit.from_dict(units_item_data)

            units.append(units_item)

        instrument_types = []
        _instrument_types = d.pop("instrument_types", UNSET)
        for instrument_types_item_data in _instrument_types or []:
            instrument_types_item = InstrumentType.from_dict(instrument_types_item_data)

            instrument_types.append(instrument_types_item)

        resource_categories = []
        _resource_categories = d.pop("resource_categories", UNSET)
        for resource_categories_item_data in _resource_categories or []:
            resource_categories_item = ResourceCategory.from_dict(resource_categories_item_data)

            resource_categories.append(resource_categories_item)

        slew_policies = []
        _slew_policies = d.pop("slew_policies", UNSET)
        for slew_policies_item_data in _slew_policies or []:
            slew_policies_item = ConfigurationItem.from_dict(slew_policies_item_data)

            slew_policies.append(slew_policies_item)

        timelines = []
        _timelines = d.pop("timelines", UNSET)
        for timelines_item_data in _timelines or []:
            timelines_item = ConfigurationItem.from_dict(timelines_item_data)

            timelines.append(timelines_item)

        platform_power_profiles = []
        _platform_power_profiles = d.pop("platform_power_profiles", UNSET)
        for platform_power_profiles_item_data in _platform_power_profiles or []:
            platform_power_profiles_item = PlatformPowerProfile.from_dict(platform_power_profiles_item_data)

            platform_power_profiles.append(platform_power_profiles_item)

        configuration = cls(
            version=version,
            targets=targets,
            instruments=instruments,
            units=units,
            instrument_types=instrument_types,
            resource_categories=resource_categories,
            slew_policies=slew_policies,
            timelines=timelines,
            platform_power_profiles=platform_power_profiles,
        )

        configuration.additional_properties = d
        return configuration

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
