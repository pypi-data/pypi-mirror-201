from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.event_types_enum import EventTypesEnum
from ..models.request_method_enum import RequestMethodEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patched_table_webhook_update_request_headers import PatchedTableWebhookUpdateRequestHeaders


T = TypeVar("T", bound="PatchedTableWebhookUpdateRequest")


@attr.s(auto_attribs=True)
class PatchedTableWebhookUpdateRequest:
    """
    Attributes:
        url (Union[Unset, str]): The URL that must be called when the webhook is triggered.
        include_all_events (Union[Unset, bool]): Indicates whether this webhook should listen to all events.
        events (Union[Unset, List[EventTypesEnum]]): A list containing the events that will trigger this webhook.
        request_method (Union[Unset, RequestMethodEnum]):
        headers (Union[Unset, PatchedTableWebhookUpdateRequestHeaders]): The additional headers as an object where the
            key is the name and the value the value.
        name (Union[Unset, str]): An internal name of the webhook.
        active (Union[Unset, bool]): Indicates whether the web hook is active. When a webhook has failed multiple times,
            it will automatically be deactivated.
        use_user_field_names (Union[Unset, bool]): Indicates whether the field names must be used as payload key instead
            of the id.
    """

    url: Union[Unset, str] = UNSET
    include_all_events: Union[Unset, bool] = UNSET
    events: Union[Unset, List[EventTypesEnum]] = UNSET
    request_method: Union[Unset, RequestMethodEnum] = UNSET
    headers: Union[Unset, "PatchedTableWebhookUpdateRequestHeaders"] = UNSET
    name: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    use_user_field_names: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        include_all_events = self.include_all_events
        events: Union[Unset, List[str]] = UNSET
        if not isinstance(self.events, Unset):
            events = []
            for events_item_data in self.events:
                events_item = events_item_data.value

                events.append(events_item)

        request_method: Union[Unset, str] = UNSET
        if not isinstance(self.request_method, Unset):
            request_method = self.request_method.value

        headers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.headers, Unset):
            headers = self.headers.to_dict()

        name = self.name
        active = self.active
        use_user_field_names = self.use_user_field_names

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if include_all_events is not UNSET:
            field_dict["include_all_events"] = include_all_events
        if events is not UNSET:
            field_dict["events"] = events
        if request_method is not UNSET:
            field_dict["request_method"] = request_method
        if headers is not UNSET:
            field_dict["headers"] = headers
        if name is not UNSET:
            field_dict["name"] = name
        if active is not UNSET:
            field_dict["active"] = active
        if use_user_field_names is not UNSET:
            field_dict["use_user_field_names"] = use_user_field_names

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.patched_table_webhook_update_request_headers import PatchedTableWebhookUpdateRequestHeaders

        d = src_dict.copy()
        url = d.pop("url", UNSET)

        include_all_events = d.pop("include_all_events", UNSET)

        events = []
        _events = d.pop("events", UNSET)
        for events_item_data in _events or []:
            events_item = EventTypesEnum(events_item_data)

            events.append(events_item)

        _request_method = d.pop("request_method", UNSET)
        request_method: Union[Unset, RequestMethodEnum]
        if isinstance(_request_method, Unset):
            request_method = UNSET
        else:
            request_method = RequestMethodEnum(_request_method)

        _headers = d.pop("headers", UNSET)
        headers: Union[Unset, PatchedTableWebhookUpdateRequestHeaders]
        if isinstance(_headers, Unset):
            headers = UNSET
        else:
            headers = PatchedTableWebhookUpdateRequestHeaders.from_dict(_headers)

        name = d.pop("name", UNSET)

        active = d.pop("active", UNSET)

        use_user_field_names = d.pop("use_user_field_names", UNSET)

        patched_table_webhook_update_request = cls(
            url=url,
            include_all_events=include_all_events,
            events=events,
            request_method=request_method,
            headers=headers,
            name=name,
            active=active,
            use_user_field_names=use_user_field_names,
        )

        patched_table_webhook_update_request.additional_properties = d
        return patched_table_webhook_update_request

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
