from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.report_failing_rows_additional_property import ReportFailingRowsAdditionalProperty


T = TypeVar("T", bound="ReportFailingRows")


@attr.s(auto_attribs=True)
class ReportFailingRows:
    """An object containing field in error by rows. The keys are the row indexes from original file and values are objects
    of errors by fields.

    """

    additional_properties: Dict[str, "ReportFailingRowsAdditionalProperty"] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.report_failing_rows_additional_property import ReportFailingRowsAdditionalProperty

        d = src_dict.copy()
        report_failing_rows = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ReportFailingRowsAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        report_failing_rows.additional_properties = additional_properties
        return report_failing_rows

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "ReportFailingRowsAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "ReportFailingRowsAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
