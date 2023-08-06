from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ActionScopes")


@attr.s(auto_attribs=True)
class ActionScopes:
    """Mixin to a DRF serializer class to raise an exception if data with unknown fields
    is provided to the serializer.

        Attributes:
            root (Union[Unset, None, bool]): If set to true then actions registered in the root scope will be included when
                undoing or redoing.
            workspace (Union[Unset, None, int]): If set to a workspaces id then any actions directly related to that
                workspace will be be included when undoing or redoing.
            group (Union[Unset, None, int]): If set to a workspaces id then any actions directly related to that workspace
                will be be included when undoing or redoing.
            application (Union[Unset, None, int]): If set to an applications id then any actions directly related to that
                application will be be included when undoing or redoing.
            table (Union[Unset, None, int]): If set to a table id then any actions directly related to that table will be be
                included when undoing or redoing.
            view (Union[Unset, None, int]): If set to an view id then any actions directly related to that view will be be
                included when undoing or redoing.
            teams_in_workspace (Union[Unset, None, int]): If set to a workspace id then any actions directly related to that
                workspace will be be included when undoing or redoing.
    """

    root: Union[Unset, None, bool] = UNSET
    workspace: Union[Unset, None, int] = UNSET
    group: Union[Unset, None, int] = UNSET
    application: Union[Unset, None, int] = UNSET
    table: Union[Unset, None, int] = UNSET
    view: Union[Unset, None, int] = UNSET
    teams_in_workspace: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        root = self.root
        workspace = self.workspace
        group = self.group
        application = self.application
        table = self.table
        view = self.view
        teams_in_workspace = self.teams_in_workspace

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if root is not UNSET:
            field_dict["root"] = root
        if workspace is not UNSET:
            field_dict["workspace"] = workspace
        if group is not UNSET:
            field_dict["group"] = group
        if application is not UNSET:
            field_dict["application"] = application
        if table is not UNSET:
            field_dict["table"] = table
        if view is not UNSET:
            field_dict["view"] = view
        if teams_in_workspace is not UNSET:
            field_dict["teams_in_workspace"] = teams_in_workspace

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        root = d.pop("root", UNSET)

        workspace = d.pop("workspace", UNSET)

        group = d.pop("group", UNSET)

        application = d.pop("application", UNSET)

        table = d.pop("table", UNSET)

        view = d.pop("view", UNSET)

        teams_in_workspace = d.pop("teams_in_workspace", UNSET)

        action_scopes = cls(
            root=root,
            workspace=workspace,
            group=group,
            application=application,
            table=table,
            view=view,
            teams_in_workspace=teams_in_workspace,
        )

        action_scopes.additional_properties = d
        return action_scopes

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
