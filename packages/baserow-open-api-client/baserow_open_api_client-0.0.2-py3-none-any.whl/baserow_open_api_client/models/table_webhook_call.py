import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TableWebhookCall")


@attr.s(auto_attribs=True)
class TableWebhookCall:
    """
    Attributes:
        id (int):
        event_id (str): Event ID where the call originated from.
        event_type (str):
        called_url (str):
        called_time (Union[Unset, None, datetime.datetime]):
        request (Union[Unset, None, str]): A text copy of the request headers and body.
        response (Union[Unset, None, str]): A text copy of the response headers and body.
        response_status (Union[Unset, None, int]): The HTTP response status code.
        error (Union[Unset, None, str]): An internal error reflecting what went wrong.
    """

    id: int
    event_id: str
    event_type: str
    called_url: str
    called_time: Union[Unset, None, datetime.datetime] = UNSET
    request: Union[Unset, None, str] = UNSET
    response: Union[Unset, None, str] = UNSET
    response_status: Union[Unset, None, int] = UNSET
    error: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        event_id = self.event_id
        event_type = self.event_type
        called_url = self.called_url
        called_time: Union[Unset, None, str] = UNSET
        if not isinstance(self.called_time, Unset):
            called_time = self.called_time.isoformat() if self.called_time else None

        request = self.request
        response = self.response
        response_status = self.response_status
        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "event_id": event_id,
                "event_type": event_type,
                "called_url": called_url,
            }
        )
        if called_time is not UNSET:
            field_dict["called_time"] = called_time
        if request is not UNSET:
            field_dict["request"] = request
        if response is not UNSET:
            field_dict["response"] = response
        if response_status is not UNSET:
            field_dict["response_status"] = response_status
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        event_id = d.pop("event_id")

        event_type = d.pop("event_type")

        called_url = d.pop("called_url")

        _called_time = d.pop("called_time", UNSET)
        called_time: Union[Unset, None, datetime.datetime]
        if _called_time is None:
            called_time = None
        elif isinstance(_called_time, Unset):
            called_time = UNSET
        else:
            called_time = isoparse(_called_time)

        request = d.pop("request", UNSET)

        response = d.pop("response", UNSET)

        response_status = d.pop("response_status", UNSET)

        error = d.pop("error", UNSET)

        table_webhook_call = cls(
            id=id,
            event_id=event_id,
            event_type=event_type,
            called_url=called_url,
            called_time=called_time,
            request=request,
            response=response,
            response_status=response_status,
            error=error,
        )

        table_webhook_call.additional_properties = d
        return table_webhook_call

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
