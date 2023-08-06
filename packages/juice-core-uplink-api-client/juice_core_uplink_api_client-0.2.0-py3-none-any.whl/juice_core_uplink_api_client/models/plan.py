from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.segment import Segment
    from ..models.segment_group import SegmentGroup


T = TypeVar("T", bound="Plan")


@attr.s(auto_attribs=True)
class Plan:
    """
    Attributes:
        trajectory (str):
        mnemonic (str):
        name (str):
        is_public (bool):
        segments (List['Segment']):
        segment_groups (List['SegmentGroup']):
        description (Union[Unset, None, str]):
        default_block (Union[Unset, str]):
        default_slew_policy (Union[Unset, str]):
        spice_info (Union[Unset, str]):
        refine_log (Union[Unset, str]):
    """

    trajectory: str
    mnemonic: str
    name: str
    is_public: bool
    segments: List["Segment"]
    segment_groups: List["SegmentGroup"]
    description: Union[Unset, None, str] = UNSET
    default_block: Union[Unset, str] = UNSET
    default_slew_policy: Union[Unset, str] = UNSET
    spice_info: Union[Unset, str] = UNSET
    refine_log: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trajectory = self.trajectory
        mnemonic = self.mnemonic
        name = self.name
        is_public = self.is_public
        segments = []
        for segments_item_data in self.segments:
            segments_item = segments_item_data.to_dict()

            segments.append(segments_item)

        segment_groups = []
        for segment_groups_item_data in self.segment_groups:
            segment_groups_item = segment_groups_item_data.to_dict()

            segment_groups.append(segment_groups_item)

        description = self.description
        default_block = self.default_block
        default_slew_policy = self.default_slew_policy
        spice_info = self.spice_info
        refine_log = self.refine_log

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trajectory": trajectory,
                "mnemonic": mnemonic,
                "name": name,
                "is_public": is_public,
                "segments": segments,
                "segment_groups": segment_groups,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if default_block is not UNSET:
            field_dict["default_block"] = default_block
        if default_slew_policy is not UNSET:
            field_dict["default_slew_policy"] = default_slew_policy
        if spice_info is not UNSET:
            field_dict["spice_info"] = spice_info
        if refine_log is not UNSET:
            field_dict["refine_log"] = refine_log

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.segment import Segment
        from ..models.segment_group import SegmentGroup

        d = src_dict.copy()
        trajectory = d.pop("trajectory")

        mnemonic = d.pop("mnemonic")

        name = d.pop("name")

        is_public = d.pop("is_public")

        segments = []
        _segments = d.pop("segments")
        for segments_item_data in _segments:
            segments_item = Segment.from_dict(segments_item_data)

            segments.append(segments_item)

        segment_groups = []
        _segment_groups = d.pop("segment_groups")
        for segment_groups_item_data in _segment_groups:
            segment_groups_item = SegmentGroup.from_dict(segment_groups_item_data)

            segment_groups.append(segment_groups_item)

        description = d.pop("description", UNSET)

        default_block = d.pop("default_block", UNSET)

        default_slew_policy = d.pop("default_slew_policy", UNSET)

        spice_info = d.pop("spice_info", UNSET)

        refine_log = d.pop("refine_log", UNSET)

        plan = cls(
            trajectory=trajectory,
            mnemonic=mnemonic,
            name=name,
            is_public=is_public,
            segments=segments,
            segment_groups=segment_groups,
            description=description,
            default_block=default_block,
            default_slew_policy=default_slew_policy,
            spice_info=spice_info,
            refine_log=refine_log,
        )

        plan.additional_properties = d
        return plan

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
