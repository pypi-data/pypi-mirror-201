from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="TableWebhookTestCallResponse")


@attr.s(auto_attribs=True)
class TableWebhookTestCallResponse:
    """
    Attributes:
        request (str): A text copy of the request headers and body.
        response (str): A text copy of the response headers and body.
        status_code (int): The HTTP response status code.
        is_unreachable (bool): Indicates whether the provided URL could be reached.
    """

    request: str
    response: str
    status_code: int
    is_unreachable: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request = self.request
        response = self.response
        status_code = self.status_code
        is_unreachable = self.is_unreachable

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "request": request,
                "response": response,
                "status_code": status_code,
                "is_unreachable": is_unreachable,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request = d.pop("request")

        response = d.pop("response")

        status_code = d.pop("status_code")

        is_unreachable = d.pop("is_unreachable")

        table_webhook_test_call_response = cls(
            request=request,
            response=response,
            status_code=status_code,
            is_unreachable=is_unreachable,
        )

        table_webhook_test_call_response.additional_properties = d
        return table_webhook_test_call_response

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
