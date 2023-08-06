from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.phase import Phase


T = TypeVar("T", bound="Trajectory")


@attr.s(auto_attribs=True)
class Trajectory:
    """
    Attributes:
        name (str):
        mnemonic (str):
        phases (List['Phase']):
        id (Union[Unset, int]):
        trajectory_type (Union[Unset, str]):
        spice_info (Union[Unset, str]):
        ptr_file (Union[Unset, str]):
    """

    name: str
    mnemonic: str
    phases: List["Phase"]
    id: Union[Unset, int] = UNSET
    trajectory_type: Union[Unset, str] = UNSET
    spice_info: Union[Unset, str] = UNSET
    ptr_file: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        mnemonic = self.mnemonic
        phases = []
        for phases_item_data in self.phases:
            phases_item = phases_item_data.to_dict()

            phases.append(phases_item)

        id = self.id
        trajectory_type = self.trajectory_type
        spice_info = self.spice_info
        ptr_file = self.ptr_file

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
                "phases": phases,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if trajectory_type is not UNSET:
            field_dict["trajectory_type"] = trajectory_type
        if spice_info is not UNSET:
            field_dict["spice_info"] = spice_info
        if ptr_file is not UNSET:
            field_dict["ptr_file"] = ptr_file

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.phase import Phase

        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        phases = []
        _phases = d.pop("phases")
        for phases_item_data in _phases:
            phases_item = Phase.from_dict(phases_item_data)

            phases.append(phases_item)

        id = d.pop("id", UNSET)

        trajectory_type = d.pop("trajectory_type", UNSET)

        spice_info = d.pop("spice_info", UNSET)

        ptr_file = d.pop("ptr_file", UNSET)

        trajectory = cls(
            name=name,
            mnemonic=mnemonic,
            phases=phases,
            id=id,
            trajectory_type=trajectory_type,
            spice_info=spice_info,
            ptr_file=ptr_file,
        )

        trajectory.additional_properties = d
        return trajectory

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
