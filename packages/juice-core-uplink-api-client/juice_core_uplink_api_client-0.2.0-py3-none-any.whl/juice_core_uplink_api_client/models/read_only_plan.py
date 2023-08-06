from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.read_only_segment_group import ReadOnlySegmentGroup


T = TypeVar("T", bound="ReadOnlyPlan")


@attr.s(auto_attribs=True)
class ReadOnlyPlan:
    """
    Attributes:
        trajectory (str):
        mnemonic (str):
        name (str):
        is_public (bool):
        segment_groups (List['ReadOnlySegmentGroup']):
        description (Union[Unset, None, str]):
        segments (Union[Unset, str]):
        refine_log (Union[Unset, str]):
        spice_info (Union[Unset, str]):
        default_block (Union[Unset, str]):
        default_slew_policy (Union[Unset, str]):
    """

    trajectory: str
    mnemonic: str
    name: str
    is_public: bool
    segment_groups: List["ReadOnlySegmentGroup"]
    description: Union[Unset, None, str] = UNSET
    segments: Union[Unset, str] = UNSET
    refine_log: Union[Unset, str] = UNSET
    spice_info: Union[Unset, str] = UNSET
    default_block: Union[Unset, str] = UNSET
    default_slew_policy: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trajectory = self.trajectory
        mnemonic = self.mnemonic
        name = self.name
        is_public = self.is_public
        segment_groups = []
        for segment_groups_item_data in self.segment_groups:
            segment_groups_item = segment_groups_item_data.to_dict()

            segment_groups.append(segment_groups_item)

        description = self.description
        segments = self.segments
        refine_log = self.refine_log
        spice_info = self.spice_info
        default_block = self.default_block
        default_slew_policy = self.default_slew_policy

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trajectory": trajectory,
                "mnemonic": mnemonic,
                "name": name,
                "is_public": is_public,
                "segment_groups": segment_groups,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if segments is not UNSET:
            field_dict["segments"] = segments
        if refine_log is not UNSET:
            field_dict["refine_log"] = refine_log
        if spice_info is not UNSET:
            field_dict["spice_info"] = spice_info
        if default_block is not UNSET:
            field_dict["default_block"] = default_block
        if default_slew_policy is not UNSET:
            field_dict["default_slew_policy"] = default_slew_policy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.read_only_segment_group import ReadOnlySegmentGroup

        d = src_dict.copy()
        trajectory = d.pop("trajectory")

        mnemonic = d.pop("mnemonic")

        name = d.pop("name")

        is_public = d.pop("is_public")

        segment_groups = []
        _segment_groups = d.pop("segment_groups")
        for segment_groups_item_data in _segment_groups:
            segment_groups_item = ReadOnlySegmentGroup.from_dict(segment_groups_item_data)

            segment_groups.append(segment_groups_item)

        description = d.pop("description", UNSET)

        segments = d.pop("segments", UNSET)

        refine_log = d.pop("refine_log", UNSET)

        spice_info = d.pop("spice_info", UNSET)

        default_block = d.pop("default_block", UNSET)

        default_slew_policy = d.pop("default_slew_policy", UNSET)

        read_only_plan = cls(
            trajectory=trajectory,
            mnemonic=mnemonic,
            name=name,
            is_public=is_public,
            segment_groups=segment_groups,
            description=description,
            segments=segments,
            refine_log=refine_log,
            spice_info=spice_info,
            default_block=default_block,
            default_slew_policy=default_slew_policy,
        )

        read_only_plan.additional_properties = d
        return read_only_plan

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
