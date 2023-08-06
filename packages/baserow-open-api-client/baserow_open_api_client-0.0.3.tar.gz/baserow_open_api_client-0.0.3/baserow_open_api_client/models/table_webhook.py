import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.request_method_enum import RequestMethodEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.table_webhook_call import TableWebhookCall
    from ..models.table_webhook_events import TableWebhookEvents
    from ..models.table_webhook_headers import TableWebhookHeaders


T = TypeVar("T", bound="TableWebhook")


@attr.s(auto_attribs=True)
class TableWebhook:
    """
    Attributes:
        id (int):
        events (TableWebhookEvents): A list containing the events that will trigger this webhook.
        headers (TableWebhookHeaders): The additional headers as an object where the key is the name and the value the
            value.
        calls (List['TableWebhookCall']): All the calls that this webhook made.
        created_on (datetime.datetime):
        updated_on (datetime.datetime):
        url (str): The URL that must be called when the webhook is triggered.
        name (str): An internal name of the webhook.
        use_user_field_names (Union[Unset, bool]): Indicates whether the field names must be used as payload key instead
            of the id.
        request_method (Union[Unset, RequestMethodEnum]):
        include_all_events (Union[Unset, bool]): Indicates whether this webhook should listen to all events.
        failed_triggers (Union[Unset, int]): The amount of failed webhook calls.
        active (Union[Unset, bool]): Indicates whether the web hook is active. When a webhook has failed multiple times,
            it will automatically be deactivated.
    """

    id: int
    events: "TableWebhookEvents"
    headers: "TableWebhookHeaders"
    calls: List["TableWebhookCall"]
    created_on: datetime.datetime
    updated_on: datetime.datetime
    url: str
    name: str
    use_user_field_names: Union[Unset, bool] = UNSET
    request_method: Union[Unset, RequestMethodEnum] = UNSET
    include_all_events: Union[Unset, bool] = UNSET
    failed_triggers: Union[Unset, int] = UNSET
    active: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        events = self.events.to_dict()

        headers = self.headers.to_dict()

        calls = []
        for calls_item_data in self.calls:
            calls_item = calls_item_data.to_dict()

            calls.append(calls_item)

        created_on = self.created_on.isoformat()

        updated_on = self.updated_on.isoformat()

        url = self.url
        name = self.name
        use_user_field_names = self.use_user_field_names
        request_method: Union[Unset, str] = UNSET
        if not isinstance(self.request_method, Unset):
            request_method = self.request_method.value

        include_all_events = self.include_all_events
        failed_triggers = self.failed_triggers
        active = self.active

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "events": events,
                "headers": headers,
                "calls": calls,
                "created_on": created_on,
                "updated_on": updated_on,
                "url": url,
                "name": name,
            }
        )
        if use_user_field_names is not UNSET:
            field_dict["use_user_field_names"] = use_user_field_names
        if request_method is not UNSET:
            field_dict["request_method"] = request_method
        if include_all_events is not UNSET:
            field_dict["include_all_events"] = include_all_events
        if failed_triggers is not UNSET:
            field_dict["failed_triggers"] = failed_triggers
        if active is not UNSET:
            field_dict["active"] = active

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.table_webhook_call import TableWebhookCall
        from ..models.table_webhook_events import TableWebhookEvents
        from ..models.table_webhook_headers import TableWebhookHeaders

        d = src_dict.copy()
        id = d.pop("id")

        events = TableWebhookEvents.from_dict(d.pop("events"))

        headers = TableWebhookHeaders.from_dict(d.pop("headers"))

        calls = []
        _calls = d.pop("calls")
        for calls_item_data in _calls:
            calls_item = TableWebhookCall.from_dict(calls_item_data)

            calls.append(calls_item)

        created_on = isoparse(d.pop("created_on"))

        updated_on = isoparse(d.pop("updated_on"))

        url = d.pop("url")

        name = d.pop("name")

        use_user_field_names = d.pop("use_user_field_names", UNSET)

        _request_method = d.pop("request_method", UNSET)
        request_method: Union[Unset, RequestMethodEnum]
        if isinstance(_request_method, Unset):
            request_method = UNSET
        else:
            request_method = RequestMethodEnum(_request_method)

        include_all_events = d.pop("include_all_events", UNSET)

        failed_triggers = d.pop("failed_triggers", UNSET)

        active = d.pop("active", UNSET)

        table_webhook = cls(
            id=id,
            events=events,
            headers=headers,
            calls=calls,
            created_on=created_on,
            updated_on=updated_on,
            url=url,
            name=name,
            use_user_field_names=use_user_field_names,
            request_method=request_method,
            include_all_events=include_all_events,
            failed_triggers=failed_triggers,
            active=active,
        )

        table_webhook.additional_properties = d
        return table_webhook

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
