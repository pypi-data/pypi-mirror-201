from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.workspace_create_team_response_404_error import WorkspaceCreateTeamResponse404Error
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workspace_create_team_response_404_detail_type_1 import WorkspaceCreateTeamResponse404DetailType1


T = TypeVar("T", bound="WorkspaceCreateTeamResponse404")


@attr.s(auto_attribs=True)
class WorkspaceCreateTeamResponse404:
    """
    Attributes:
        error (Union[Unset, WorkspaceCreateTeamResponse404Error]): Machine readable error indicating what went wrong.
        detail (Union['WorkspaceCreateTeamResponse404DetailType1', Unset, str]):
    """

    error: Union[Unset, WorkspaceCreateTeamResponse404Error] = UNSET
    detail: Union["WorkspaceCreateTeamResponse404DetailType1", Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.workspace_create_team_response_404_detail_type_1 import WorkspaceCreateTeamResponse404DetailType1

        error: Union[Unset, str] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.value

        detail: Union[Dict[str, Any], Unset, str]
        if isinstance(self.detail, Unset):
            detail = UNSET

        elif isinstance(self.detail, WorkspaceCreateTeamResponse404DetailType1):
            detail = UNSET
            if not isinstance(self.detail, Unset):
                detail = self.detail.to_dict()

        else:
            detail = self.detail

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error
        if detail is not UNSET:
            field_dict["detail"] = detail

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workspace_create_team_response_404_detail_type_1 import WorkspaceCreateTeamResponse404DetailType1

        d = src_dict.copy()
        _error = d.pop("error", UNSET)
        error: Union[Unset, WorkspaceCreateTeamResponse404Error]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = WorkspaceCreateTeamResponse404Error(_error)

        def _parse_detail(data: object) -> Union["WorkspaceCreateTeamResponse404DetailType1", Unset, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _detail_type_1 = data
                detail_type_1: Union[Unset, WorkspaceCreateTeamResponse404DetailType1]
                if isinstance(_detail_type_1, Unset):
                    detail_type_1 = UNSET
                else:
                    detail_type_1 = WorkspaceCreateTeamResponse404DetailType1.from_dict(_detail_type_1)

                return detail_type_1
            except:  # noqa: E722
                pass
            return cast(Union["WorkspaceCreateTeamResponse404DetailType1", Unset, str], data)

        detail = _parse_detail(d.pop("detail", UNSET))

        workspace_create_team_response_404 = cls(
            error=error,
            detail=detail,
        )

        workspace_create_team_response_404.additional_properties = d
        return workspace_create_team_response_404

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
