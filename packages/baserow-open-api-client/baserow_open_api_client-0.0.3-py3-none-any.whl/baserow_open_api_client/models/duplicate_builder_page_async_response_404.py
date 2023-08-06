from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.duplicate_builder_page_async_response_404_error import DuplicateBuilderPageAsyncResponse404Error
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.duplicate_builder_page_async_response_404_detail_type_1 import (
        DuplicateBuilderPageAsyncResponse404DetailType1,
    )


T = TypeVar("T", bound="DuplicateBuilderPageAsyncResponse404")


@attr.s(auto_attribs=True)
class DuplicateBuilderPageAsyncResponse404:
    """
    Attributes:
        error (Union[Unset, DuplicateBuilderPageAsyncResponse404Error]): Machine readable error indicating what went
            wrong.
        detail (Union['DuplicateBuilderPageAsyncResponse404DetailType1', Unset, str]):
    """

    error: Union[Unset, DuplicateBuilderPageAsyncResponse404Error] = UNSET
    detail: Union["DuplicateBuilderPageAsyncResponse404DetailType1", Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.duplicate_builder_page_async_response_404_detail_type_1 import (
            DuplicateBuilderPageAsyncResponse404DetailType1,
        )

        error: Union[Unset, str] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.value

        detail: Union[Dict[str, Any], Unset, str]
        if isinstance(self.detail, Unset):
            detail = UNSET

        elif isinstance(self.detail, DuplicateBuilderPageAsyncResponse404DetailType1):
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
        from ..models.duplicate_builder_page_async_response_404_detail_type_1 import (
            DuplicateBuilderPageAsyncResponse404DetailType1,
        )

        d = src_dict.copy()
        _error = d.pop("error", UNSET)
        error: Union[Unset, DuplicateBuilderPageAsyncResponse404Error]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = DuplicateBuilderPageAsyncResponse404Error(_error)

        def _parse_detail(data: object) -> Union["DuplicateBuilderPageAsyncResponse404DetailType1", Unset, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _detail_type_1 = data
                detail_type_1: Union[Unset, DuplicateBuilderPageAsyncResponse404DetailType1]
                if isinstance(_detail_type_1, Unset):
                    detail_type_1 = UNSET
                else:
                    detail_type_1 = DuplicateBuilderPageAsyncResponse404DetailType1.from_dict(_detail_type_1)

                return detail_type_1
            except:  # noqa: E722
                pass
            return cast(Union["DuplicateBuilderPageAsyncResponse404DetailType1", Unset, str], data)

        detail = _parse_detail(d.pop("detail", UNSET))

        duplicate_builder_page_async_response_404 = cls(
            error=error,
            detail=detail,
        )

        duplicate_builder_page_async_response_404.additional_properties = d
        return duplicate_builder_page_async_response_404

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
