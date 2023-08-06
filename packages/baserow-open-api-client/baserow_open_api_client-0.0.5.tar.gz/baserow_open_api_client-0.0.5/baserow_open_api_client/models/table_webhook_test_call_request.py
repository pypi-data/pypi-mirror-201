from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.event_type_enum import EventTypeEnum
from ..models.request_method_enum import RequestMethodEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.table_webhook_test_call_request_headers import TableWebhookTestCallRequestHeaders


T = TypeVar("T", bound="TableWebhookTestCallRequest")


@attr.s(auto_attribs=True)
class TableWebhookTestCallRequest:
    """
    Attributes:
        url (str): The URL that must be called when the webhook is triggered.
        event_type (EventTypeEnum):
        request_method (Union[Unset, RequestMethodEnum]):
        headers (Union[Unset, TableWebhookTestCallRequestHeaders]): The additional headers as an object where the key is
            the name and the value the value.
        use_user_field_names (Union[Unset, bool]): Indicates whether the field names must be used as payload key instead
            of the id.
    """

    url: str
    event_type: EventTypeEnum
    request_method: Union[Unset, RequestMethodEnum] = UNSET
    headers: Union[Unset, "TableWebhookTestCallRequestHeaders"] = UNSET
    use_user_field_names: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        event_type = self.event_type.value

        request_method: Union[Unset, str] = UNSET
        if not isinstance(self.request_method, Unset):
            request_method = self.request_method.value

        headers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.headers, Unset):
            headers = self.headers.to_dict()

        use_user_field_names = self.use_user_field_names

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "event_type": event_type,
            }
        )
        if request_method is not UNSET:
            field_dict["request_method"] = request_method
        if headers is not UNSET:
            field_dict["headers"] = headers
        if use_user_field_names is not UNSET:
            field_dict["use_user_field_names"] = use_user_field_names

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.table_webhook_test_call_request_headers import TableWebhookTestCallRequestHeaders

        d = src_dict.copy()
        url = d.pop("url")

        event_type = EventTypeEnum(d.pop("event_type"))

        _request_method = d.pop("request_method", UNSET)
        request_method: Union[Unset, RequestMethodEnum]
        if isinstance(_request_method, Unset):
            request_method = UNSET
        else:
            request_method = RequestMethodEnum(_request_method)

        _headers = d.pop("headers", UNSET)
        headers: Union[Unset, TableWebhookTestCallRequestHeaders]
        if isinstance(_headers, Unset):
            headers = UNSET
        else:
            headers = TableWebhookTestCallRequestHeaders.from_dict(_headers)

        use_user_field_names = d.pop("use_user_field_names", UNSET)

        table_webhook_test_call_request = cls(
            url=url,
            event_type=event_type,
            request_method=request_method,
            headers=headers,
            use_user_field_names=use_user_field_names,
        )

        table_webhook_test_call_request.additional_properties = d
        return table_webhook_test_call_request

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
