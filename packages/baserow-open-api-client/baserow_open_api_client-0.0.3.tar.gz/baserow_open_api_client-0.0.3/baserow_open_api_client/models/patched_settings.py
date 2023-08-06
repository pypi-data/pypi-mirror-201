from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedSettings")


@attr.s(auto_attribs=True)
class PatchedSettings:
    """
    Attributes:
        allow_new_signups (Union[Unset, bool]): Indicates whether new users can create a new account when signing up.
        allow_signups_via_workspace_invitations (Union[Unset, bool]): Indicates whether invited users can create an
            account when signing up, even if allow_new_signups is disabled.
        allow_signups_via_group_invitations (Union[Unset, bool]): DEPRECATED: Please use the functionally identical
            `allow_signups_via_workspace_invitations` instead as this attribute is being removed in the future.
        allow_reset_password (Union[Unset, bool]): Indicates whether users can request a password reset link.
        allow_global_workspace_creation (Union[Unset, bool]): Indicates whether all users can create workspaces, or just
            staff.
        allow_global_group_creation (Union[Unset, bool]): DEPRECATED: Please use the functionally identical
            `allow_global_workspace_creation` instead as this attribute is being removed in the future.
        account_deletion_grace_delay (Union[Unset, int]): Number of days after the last login for an account pending
            deletion to be deleted
        show_admin_signup_page (Union[Unset, bool]): Indicates that there are no admin users in the database yet, so in
            the frontend the signup form will be shown instead of the login page.
        track_workspace_usage (Union[Unset, bool]): Runs a job once per day which calculates per workspace row counts
            and file storage usage, displayed on the admin workspace page.
    """

    allow_new_signups: Union[Unset, bool] = UNSET
    allow_signups_via_workspace_invitations: Union[Unset, bool] = UNSET
    allow_signups_via_group_invitations: Union[Unset, bool] = UNSET
    allow_reset_password: Union[Unset, bool] = UNSET
    allow_global_workspace_creation: Union[Unset, bool] = UNSET
    allow_global_group_creation: Union[Unset, bool] = UNSET
    account_deletion_grace_delay: Union[Unset, int] = UNSET
    show_admin_signup_page: Union[Unset, bool] = UNSET
    track_workspace_usage: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        allow_new_signups = self.allow_new_signups
        allow_signups_via_workspace_invitations = self.allow_signups_via_workspace_invitations
        allow_signups_via_group_invitations = self.allow_signups_via_group_invitations
        allow_reset_password = self.allow_reset_password
        allow_global_workspace_creation = self.allow_global_workspace_creation
        allow_global_group_creation = self.allow_global_group_creation
        account_deletion_grace_delay = self.account_deletion_grace_delay
        show_admin_signup_page = self.show_admin_signup_page
        track_workspace_usage = self.track_workspace_usage

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allow_new_signups is not UNSET:
            field_dict["allow_new_signups"] = allow_new_signups
        if allow_signups_via_workspace_invitations is not UNSET:
            field_dict["allow_signups_via_workspace_invitations"] = allow_signups_via_workspace_invitations
        if allow_signups_via_group_invitations is not UNSET:
            field_dict["allow_signups_via_group_invitations"] = allow_signups_via_group_invitations
        if allow_reset_password is not UNSET:
            field_dict["allow_reset_password"] = allow_reset_password
        if allow_global_workspace_creation is not UNSET:
            field_dict["allow_global_workspace_creation"] = allow_global_workspace_creation
        if allow_global_group_creation is not UNSET:
            field_dict["allow_global_group_creation"] = allow_global_group_creation
        if account_deletion_grace_delay is not UNSET:
            field_dict["account_deletion_grace_delay"] = account_deletion_grace_delay
        if show_admin_signup_page is not UNSET:
            field_dict["show_admin_signup_page"] = show_admin_signup_page
        if track_workspace_usage is not UNSET:
            field_dict["track_workspace_usage"] = track_workspace_usage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        allow_new_signups = d.pop("allow_new_signups", UNSET)

        allow_signups_via_workspace_invitations = d.pop("allow_signups_via_workspace_invitations", UNSET)

        allow_signups_via_group_invitations = d.pop("allow_signups_via_group_invitations", UNSET)

        allow_reset_password = d.pop("allow_reset_password", UNSET)

        allow_global_workspace_creation = d.pop("allow_global_workspace_creation", UNSET)

        allow_global_group_creation = d.pop("allow_global_group_creation", UNSET)

        account_deletion_grace_delay = d.pop("account_deletion_grace_delay", UNSET)

        show_admin_signup_page = d.pop("show_admin_signup_page", UNSET)

        track_workspace_usage = d.pop("track_workspace_usage", UNSET)

        patched_settings = cls(
            allow_new_signups=allow_new_signups,
            allow_signups_via_workspace_invitations=allow_signups_via_workspace_invitations,
            allow_signups_via_group_invitations=allow_signups_via_group_invitations,
            allow_reset_password=allow_reset_password,
            allow_global_workspace_creation=allow_global_workspace_creation,
            allow_global_group_creation=allow_global_group_creation,
            account_deletion_grace_delay=account_deletion_grace_delay,
            show_admin_signup_page=show_admin_signup_page,
            track_workspace_usage=track_workspace_usage,
        )

        patched_settings.additional_properties = d
        return patched_settings

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
