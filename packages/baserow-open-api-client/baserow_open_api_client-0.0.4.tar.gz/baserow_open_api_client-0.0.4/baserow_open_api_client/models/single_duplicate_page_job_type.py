from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.page import Page


T = TypeVar("T", bound="SingleDuplicatePageJobType")


@attr.s(auto_attribs=True)
class SingleDuplicatePageJobType:
    """
    Attributes:
        id (int):
        type (str): The type of the job.
        progress_percentage (int): A percentage indicating how far along the job is. 100 means that it's finished.
        state (str): Indicates the state of the import job.
        original_page (Page):
        duplicated_page (Page):
        human_readable_error (Union[Unset, str]): A human readable error message indicating what went wrong.
    """

    id: int
    type: str
    progress_percentage: int
    state: str
    original_page: "Page"
    duplicated_page: "Page"
    human_readable_error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        type = self.type
        progress_percentage = self.progress_percentage
        state = self.state
        original_page = self.original_page.to_dict()

        duplicated_page = self.duplicated_page.to_dict()

        human_readable_error = self.human_readable_error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type,
                "progress_percentage": progress_percentage,
                "state": state,
                "original_page": original_page,
                "duplicated_page": duplicated_page,
            }
        )
        if human_readable_error is not UNSET:
            field_dict["human_readable_error"] = human_readable_error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.page import Page

        d = src_dict.copy()
        id = d.pop("id")

        type = d.pop("type")

        progress_percentage = d.pop("progress_percentage")

        state = d.pop("state")

        original_page = Page.from_dict(d.pop("original_page"))

        duplicated_page = Page.from_dict(d.pop("duplicated_page"))

        human_readable_error = d.pop("human_readable_error", UNSET)

        single_duplicate_page_job_type = cls(
            id=id,
            type=type,
            progress_percentage=progress_percentage,
            state=state,
            original_page=original_page,
            duplicated_page=duplicated_page,
            human_readable_error=human_readable_error,
        )

        single_duplicate_page_job_type.additional_properties = d
        return single_duplicate_page_job_type

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
