from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.instrument_resource_profile import InstrumentResourceProfile
    from ..models.resource_profile import ResourceProfile


T = TypeVar("T", bound="Segment")


@attr.s(auto_attribs=True)
class Segment:
    """
    Attributes:
        start (str):
        end (str):
        segment_definition (str):
        overwritten (bool):
        instrument_overwritten (bool):
        timeline (str):
        name (Union[Unset, str]):
        resources (Union[Unset, None, List['ResourceProfile']]):
        instrument_resources (Union[Unset, None, List['InstrumentResourceProfile']]):
        segment_group (Union[Unset, None, str]):
        platform_power_profile (Union[Unset, None, str]):
        platform_power (Union[Unset, None, float]):
        pointing_request_snippet (Union[Unset, None, str]):
        slew_policy (Union[Unset, None, str]):
        pointing_target (Union[Unset, None, str]):
        scheduling_priority (Union[Unset, None, int]):
        origin (Union[Unset, None, str]):
    """

    start: str
    end: str
    segment_definition: str
    overwritten: bool
    instrument_overwritten: bool
    timeline: str
    name: Union[Unset, str] = UNSET
    resources: Union[Unset, None, List["ResourceProfile"]] = UNSET
    instrument_resources: Union[Unset, None, List["InstrumentResourceProfile"]] = UNSET
    segment_group: Union[Unset, None, str] = UNSET
    platform_power_profile: Union[Unset, None, str] = UNSET
    platform_power: Union[Unset, None, float] = UNSET
    pointing_request_snippet: Union[Unset, None, str] = UNSET
    slew_policy: Union[Unset, None, str] = UNSET
    pointing_target: Union[Unset, None, str] = UNSET
    scheduling_priority: Union[Unset, None, int] = UNSET
    origin: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start = self.start
        end = self.end
        segment_definition = self.segment_definition
        overwritten = self.overwritten
        instrument_overwritten = self.instrument_overwritten
        timeline = self.timeline
        name = self.name
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

        segment_group = self.segment_group
        platform_power_profile = self.platform_power_profile
        platform_power = self.platform_power
        pointing_request_snippet = self.pointing_request_snippet
        slew_policy = self.slew_policy
        pointing_target = self.pointing_target
        scheduling_priority = self.scheduling_priority
        origin = self.origin

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start": start,
                "end": end,
                "segment_definition": segment_definition,
                "overwritten": overwritten,
                "instrument_overwritten": instrument_overwritten,
                "timeline": timeline,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if resources is not UNSET:
            field_dict["resources"] = resources
        if instrument_resources is not UNSET:
            field_dict["instrument_resources"] = instrument_resources
        if segment_group is not UNSET:
            field_dict["segment_group"] = segment_group
        if platform_power_profile is not UNSET:
            field_dict["platform_power_profile"] = platform_power_profile
        if platform_power is not UNSET:
            field_dict["platform_power"] = platform_power
        if pointing_request_snippet is not UNSET:
            field_dict["pointing_request_snippet"] = pointing_request_snippet
        if slew_policy is not UNSET:
            field_dict["slew_policy"] = slew_policy
        if pointing_target is not UNSET:
            field_dict["pointing_target"] = pointing_target
        if scheduling_priority is not UNSET:
            field_dict["scheduling_priority"] = scheduling_priority
        if origin is not UNSET:
            field_dict["origin"] = origin

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.instrument_resource_profile import InstrumentResourceProfile
        from ..models.resource_profile import ResourceProfile

        d = src_dict.copy()
        start = d.pop("start")

        end = d.pop("end")

        segment_definition = d.pop("segment_definition")

        overwritten = d.pop("overwritten")

        instrument_overwritten = d.pop("instrument_overwritten")

        timeline = d.pop("timeline")

        name = d.pop("name", UNSET)

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

        segment_group = d.pop("segment_group", UNSET)

        platform_power_profile = d.pop("platform_power_profile", UNSET)

        platform_power = d.pop("platform_power", UNSET)

        pointing_request_snippet = d.pop("pointing_request_snippet", UNSET)

        slew_policy = d.pop("slew_policy", UNSET)

        pointing_target = d.pop("pointing_target", UNSET)

        scheduling_priority = d.pop("scheduling_priority", UNSET)

        origin = d.pop("origin", UNSET)

        segment = cls(
            start=start,
            end=end,
            segment_definition=segment_definition,
            overwritten=overwritten,
            instrument_overwritten=instrument_overwritten,
            timeline=timeline,
            name=name,
            resources=resources,
            instrument_resources=instrument_resources,
            segment_group=segment_group,
            platform_power_profile=platform_power_profile,
            platform_power=platform_power,
            pointing_request_snippet=pointing_request_snippet,
            slew_policy=slew_policy,
            pointing_target=pointing_target,
            scheduling_priority=scheduling_priority,
            origin=origin,
        )

        segment.additional_properties = d
        return segment

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
