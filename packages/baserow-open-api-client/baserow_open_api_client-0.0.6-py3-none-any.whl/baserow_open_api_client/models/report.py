from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.report_failing_rows import ReportFailingRows


T = TypeVar("T", bound="Report")


@attr.s(auto_attribs=True)
class Report:
    """
    Attributes:
        failing_rows (ReportFailingRows): An object containing field in error by rows. The keys are the row indexes from
            original file and values are objects of errors by fields.
    """

    failing_rows: "ReportFailingRows"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        failing_rows = self.failing_rows.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "failing_rows": failing_rows,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.report_failing_rows import ReportFailingRows

        d = src_dict.copy()
        failing_rows = ReportFailingRows.from_dict(d.pop("failing_rows"))

        report = cls(
            failing_rows=failing_rows,
        )

        report.additional_properties = d
        return report

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
