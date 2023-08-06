from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.segment import Segment
    from ..models.spice_kernel import SpiceKernel


T = TypeVar("T", bound="SimphonyPlan")


@attr.s(auto_attribs=True)
class SimphonyPlan:
    """
    Attributes:
        trajectory (str):
        mnemonic (str):
        is_public (bool):
        segment_timeline (List['Segment']):
        segment_opportunities (List['Segment']):
        kernels (List['SpiceKernel']):
        skd_version (str):
        metakernel (str):
        default_block (str):
        default_slew_policy (str):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
    """

    trajectory: str
    mnemonic: str
    is_public: bool
    segment_timeline: List["Segment"]
    segment_opportunities: List["Segment"]
    kernels: List["SpiceKernel"]
    skd_version: str
    metakernel: str
    default_block: str
    default_slew_policy: str
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trajectory = self.trajectory
        mnemonic = self.mnemonic
        is_public = self.is_public
        segment_timeline = []
        for segment_timeline_item_data in self.segment_timeline:
            segment_timeline_item = segment_timeline_item_data.to_dict()

            segment_timeline.append(segment_timeline_item)

        segment_opportunities = []
        for segment_opportunities_item_data in self.segment_opportunities:
            segment_opportunities_item = segment_opportunities_item_data.to_dict()

            segment_opportunities.append(segment_opportunities_item)

        kernels = []
        for kernels_item_data in self.kernels:
            kernels_item = kernels_item_data.to_dict()

            kernels.append(kernels_item)

        skd_version = self.skd_version
        metakernel = self.metakernel
        default_block = self.default_block
        default_slew_policy = self.default_slew_policy
        name = self.name
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trajectory": trajectory,
                "mnemonic": mnemonic,
                "is_public": is_public,
                "segment_timeline": segment_timeline,
                "segment_opportunities": segment_opportunities,
                "kernels": kernels,
                "skd_version": skd_version,
                "metakernel": metakernel,
                "default_block": default_block,
                "default_slew_policy": default_slew_policy,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.segment import Segment
        from ..models.spice_kernel import SpiceKernel

        d = src_dict.copy()
        trajectory = d.pop("trajectory")

        mnemonic = d.pop("mnemonic")

        is_public = d.pop("is_public")

        segment_timeline = []
        _segment_timeline = d.pop("segment_timeline")
        for segment_timeline_item_data in _segment_timeline:
            segment_timeline_item = Segment.from_dict(segment_timeline_item_data)

            segment_timeline.append(segment_timeline_item)

        segment_opportunities = []
        _segment_opportunities = d.pop("segment_opportunities")
        for segment_opportunities_item_data in _segment_opportunities:
            segment_opportunities_item = Segment.from_dict(segment_opportunities_item_data)

            segment_opportunities.append(segment_opportunities_item)

        kernels = []
        _kernels = d.pop("kernels")
        for kernels_item_data in _kernels:
            kernels_item = SpiceKernel.from_dict(kernels_item_data)

            kernels.append(kernels_item)

        skd_version = d.pop("skd_version")

        metakernel = d.pop("metakernel")

        default_block = d.pop("default_block")

        default_slew_policy = d.pop("default_slew_policy")

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        simphony_plan = cls(
            trajectory=trajectory,
            mnemonic=mnemonic,
            is_public=is_public,
            segment_timeline=segment_timeline,
            segment_opportunities=segment_opportunities,
            kernels=kernels,
            skd_version=skd_version,
            metakernel=metakernel,
            default_block=default_block,
            default_slew_policy=default_slew_policy,
            name=name,
            description=description,
        )

        simphony_plan.additional_properties = d
        return simphony_plan

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
