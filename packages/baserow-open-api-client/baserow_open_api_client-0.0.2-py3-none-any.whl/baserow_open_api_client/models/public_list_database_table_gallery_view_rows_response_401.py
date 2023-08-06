from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.public_list_database_table_gallery_view_rows_response_401_error import (
    PublicListDatabaseTableGalleryViewRowsResponse401Error,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.public_list_database_table_gallery_view_rows_response_401_detail_type_1 import (
        PublicListDatabaseTableGalleryViewRowsResponse401DetailType1,
    )


T = TypeVar("T", bound="PublicListDatabaseTableGalleryViewRowsResponse401")


@attr.s(auto_attribs=True)
class PublicListDatabaseTableGalleryViewRowsResponse401:
    """
    Attributes:
        error (Union[Unset, PublicListDatabaseTableGalleryViewRowsResponse401Error]): Machine readable error indicating
            what went wrong.
        detail (Union['PublicListDatabaseTableGalleryViewRowsResponse401DetailType1', Unset, str]):
    """

    error: Union[Unset, PublicListDatabaseTableGalleryViewRowsResponse401Error] = UNSET
    detail: Union["PublicListDatabaseTableGalleryViewRowsResponse401DetailType1", Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.public_list_database_table_gallery_view_rows_response_401_detail_type_1 import (
            PublicListDatabaseTableGalleryViewRowsResponse401DetailType1,
        )

        error: Union[Unset, str] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.value

        detail: Union[Dict[str, Any], Unset, str]
        if isinstance(self.detail, Unset):
            detail = UNSET

        elif isinstance(self.detail, PublicListDatabaseTableGalleryViewRowsResponse401DetailType1):
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
        from ..models.public_list_database_table_gallery_view_rows_response_401_detail_type_1 import (
            PublicListDatabaseTableGalleryViewRowsResponse401DetailType1,
        )

        d = src_dict.copy()
        _error = d.pop("error", UNSET)
        error: Union[Unset, PublicListDatabaseTableGalleryViewRowsResponse401Error]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = PublicListDatabaseTableGalleryViewRowsResponse401Error(_error)

        def _parse_detail(
            data: object,
        ) -> Union["PublicListDatabaseTableGalleryViewRowsResponse401DetailType1", Unset, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _detail_type_1 = data
                detail_type_1: Union[Unset, PublicListDatabaseTableGalleryViewRowsResponse401DetailType1]
                if isinstance(_detail_type_1, Unset):
                    detail_type_1 = UNSET
                else:
                    detail_type_1 = PublicListDatabaseTableGalleryViewRowsResponse401DetailType1.from_dict(
                        _detail_type_1
                    )

                return detail_type_1
            except:  # noqa: E722
                pass
            return cast(Union["PublicListDatabaseTableGalleryViewRowsResponse401DetailType1", Unset, str], data)

        detail = _parse_detail(d.pop("detail", UNSET))

        public_list_database_table_gallery_view_rows_response_401 = cls(
            error=error,
            detail=detail,
        )

        public_list_database_table_gallery_view_rows_response_401.additional_properties = d
        return public_list_database_table_gallery_view_rows_response_401

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
