from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Register")


@attr.s(auto_attribs=True)
class Register:
    """
    Attributes:
        name (str):
        email (str): The email address is also going to be the username.
        password (str):
        language (Union[Unset, str]): An ISO 639 language code (with optional variant) selected by the user. Ex: en-GB.
            Default: 'en'.
        authenticate (Union[Unset, bool]): Indicates whether an authentication JWT should be generated and be included
            in the response.
        group_invitation_token (Union[Unset, str]): DEPRECATED: Please use `workspace_invitation_token` which this
            attribute is being renamed to in 2024.
        workspace_invitation_token (Union[Unset, str]): If provided and valid, the user accepts the workspace invitation
            and will have access to the workspace after signing up.
        template_id (Union[Unset, int]): The id of the template that must be installed after creating the account. This
            only works if the `workspace_invitation_token` param is not provided.
    """

    name: str
    email: str
    password: str
    language: Union[Unset, str] = "en"
    authenticate: Union[Unset, bool] = False
    group_invitation_token: Union[Unset, str] = UNSET
    workspace_invitation_token: Union[Unset, str] = UNSET
    template_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        email = self.email
        password = self.password
        language = self.language
        authenticate = self.authenticate
        group_invitation_token = self.group_invitation_token
        workspace_invitation_token = self.workspace_invitation_token
        template_id = self.template_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "email": email,
                "password": password,
            }
        )
        if language is not UNSET:
            field_dict["language"] = language
        if authenticate is not UNSET:
            field_dict["authenticate"] = authenticate
        if group_invitation_token is not UNSET:
            field_dict["group_invitation_token"] = group_invitation_token
        if workspace_invitation_token is not UNSET:
            field_dict["workspace_invitation_token"] = workspace_invitation_token
        if template_id is not UNSET:
            field_dict["template_id"] = template_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        email = d.pop("email")

        password = d.pop("password")

        language = d.pop("language", UNSET)

        authenticate = d.pop("authenticate", UNSET)

        group_invitation_token = d.pop("group_invitation_token", UNSET)

        workspace_invitation_token = d.pop("workspace_invitation_token", UNSET)

        template_id = d.pop("template_id", UNSET)

        register = cls(
            name=name,
            email=email,
            password=password,
            language=language,
            authenticate=authenticate,
            group_invitation_token=group_invitation_token,
            workspace_invitation_token=workspace_invitation_token,
            template_id=template_id,
        )

        register.additional_properties = d
        return register

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
