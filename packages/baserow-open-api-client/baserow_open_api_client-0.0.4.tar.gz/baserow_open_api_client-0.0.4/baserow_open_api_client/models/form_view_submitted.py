from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.submit_action_enum import SubmitActionEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="FormViewSubmitted")


@attr.s(auto_attribs=True)
class FormViewSubmitted:
    """
    Attributes:
        row_id (int):
        submit_action (Union[Unset, SubmitActionEnum]):
        submit_action_message (Union[Unset, str]): If the `submit_action` is MESSAGE, then this message will be shown to
            the visitor after submitting the form.
        submit_action_redirect_url (Union[Unset, str]): If the `submit_action` is REDIRECT,then the visitors will be
            redirected to the this URL after submitting the form.
    """

    row_id: int
    submit_action: Union[Unset, SubmitActionEnum] = UNSET
    submit_action_message: Union[Unset, str] = UNSET
    submit_action_redirect_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        row_id = self.row_id
        submit_action: Union[Unset, str] = UNSET
        if not isinstance(self.submit_action, Unset):
            submit_action = self.submit_action.value

        submit_action_message = self.submit_action_message
        submit_action_redirect_url = self.submit_action_redirect_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "row_id": row_id,
            }
        )
        if submit_action is not UNSET:
            field_dict["submit_action"] = submit_action
        if submit_action_message is not UNSET:
            field_dict["submit_action_message"] = submit_action_message
        if submit_action_redirect_url is not UNSET:
            field_dict["submit_action_redirect_url"] = submit_action_redirect_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        row_id = d.pop("row_id")

        _submit_action = d.pop("submit_action", UNSET)
        submit_action: Union[Unset, SubmitActionEnum]
        if isinstance(_submit_action, Unset):
            submit_action = UNSET
        else:
            submit_action = SubmitActionEnum(_submit_action)

        submit_action_message = d.pop("submit_action_message", UNSET)

        submit_action_redirect_url = d.pop("submit_action_redirect_url", UNSET)

        form_view_submitted = cls(
            row_id=row_id,
            submit_action=submit_action,
            submit_action_message=submit_action_message,
            submit_action_redirect_url=submit_action_redirect_url,
        )

        form_view_submitted.additional_properties = d
        return form_view_submitted

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
