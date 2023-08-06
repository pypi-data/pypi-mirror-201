from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DetailedScenario")


@attr.s(auto_attribs=True)
class DetailedScenario:
    """
    Attributes:
        trajectory (str):
        mnemonic (str):
        name (str):
        id (Union[Unset, int]):
        description (Union[Unset, None, str]):
        scenario_json_file (Union[Unset, None, str]):
        start (Union[Unset, None, str]):
        end (Union[Unset, None, str]):
    """

    trajectory: str
    mnemonic: str
    name: str
    id: Union[Unset, int] = UNSET
    description: Union[Unset, None, str] = UNSET
    scenario_json_file: Union[Unset, None, str] = UNSET
    start: Union[Unset, None, str] = UNSET
    end: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trajectory = self.trajectory
        mnemonic = self.mnemonic
        name = self.name
        id = self.id
        description = self.description
        scenario_json_file = self.scenario_json_file
        start = self.start
        end = self.end

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trajectory": trajectory,
                "mnemonic": mnemonic,
                "name": name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if description is not UNSET:
            field_dict["description"] = description
        if scenario_json_file is not UNSET:
            field_dict["scenario_json_file"] = scenario_json_file
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trajectory = d.pop("trajectory")

        mnemonic = d.pop("mnemonic")

        name = d.pop("name")

        id = d.pop("id", UNSET)

        description = d.pop("description", UNSET)

        scenario_json_file = d.pop("scenario_json_file", UNSET)

        start = d.pop("start", UNSET)

        end = d.pop("end", UNSET)

        detailed_scenario = cls(
            trajectory=trajectory,
            mnemonic=mnemonic,
            name=name,
            id=id,
            description=description,
            scenario_json_file=scenario_json_file,
            start=start,
            end=end,
        )

        detailed_scenario.additional_properties = d
        return detailed_scenario

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
