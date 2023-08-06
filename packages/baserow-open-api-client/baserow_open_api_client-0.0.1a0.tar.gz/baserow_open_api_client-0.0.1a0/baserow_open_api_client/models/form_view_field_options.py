from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.condition_type_enum import ConditionTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.form_view_field_options_condition import FormViewFieldOptionsCondition


T = TypeVar("T", bound="FormViewFieldOptions")


@attr.s(auto_attribs=True)
class FormViewFieldOptions:
    """
    Attributes:
        name (Union[Unset, str]): By default, the name of the related field will be shown to the visitor. Optionally
            another name can be used by setting this name.
        description (Union[Unset, str]): If provided, then this value be will be shown under the field name.
        enabled (Union[Unset, bool]): Indicates whether the field is included in the form.
        required (Union[Unset, bool]): Indicates whether the field is required for the visitor to fill out.
        show_when_matching_conditions (Union[Unset, bool]): Indicates whether this field is visible when the conditions
            are met.
        condition_type (Union[Unset, ConditionTypeEnum]):
        order (Union[Unset, int]): The order that the field has in the form. Lower value is first.
        conditions (Union[Unset, List['FormViewFieldOptionsCondition']]):
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    required: Union[Unset, bool] = UNSET
    show_when_matching_conditions: Union[Unset, bool] = UNSET
    condition_type: Union[Unset, ConditionTypeEnum] = UNSET
    order: Union[Unset, int] = UNSET
    conditions: Union[Unset, List["FormViewFieldOptionsCondition"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        enabled = self.enabled
        required = self.required
        show_when_matching_conditions = self.show_when_matching_conditions
        condition_type: Union[Unset, str] = UNSET
        if not isinstance(self.condition_type, Unset):
            condition_type = self.condition_type.value

        order = self.order
        conditions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.conditions, Unset):
            conditions = []
            for conditions_item_data in self.conditions:
                conditions_item = conditions_item_data.to_dict()

                conditions.append(conditions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if required is not UNSET:
            field_dict["required"] = required
        if show_when_matching_conditions is not UNSET:
            field_dict["show_when_matching_conditions"] = show_when_matching_conditions
        if condition_type is not UNSET:
            field_dict["condition_type"] = condition_type
        if order is not UNSET:
            field_dict["order"] = order
        if conditions is not UNSET:
            field_dict["conditions"] = conditions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.form_view_field_options_condition import FormViewFieldOptionsCondition

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        enabled = d.pop("enabled", UNSET)

        required = d.pop("required", UNSET)

        show_when_matching_conditions = d.pop("show_when_matching_conditions", UNSET)

        _condition_type = d.pop("condition_type", UNSET)
        condition_type: Union[Unset, ConditionTypeEnum]
        if isinstance(_condition_type, Unset):
            condition_type = UNSET
        else:
            condition_type = ConditionTypeEnum(_condition_type)

        order = d.pop("order", UNSET)

        conditions = []
        _conditions = d.pop("conditions", UNSET)
        for conditions_item_data in _conditions or []:
            conditions_item = FormViewFieldOptionsCondition.from_dict(conditions_item_data)

            conditions.append(conditions_item)

        form_view_field_options = cls(
            name=name,
            description=description,
            enabled=enabled,
            required=required,
            show_when_matching_conditions=show_when_matching_conditions,
            condition_type=condition_type,
            order=order,
            conditions=conditions,
        )

        form_view_field_options.additional_properties = d
        return form_view_field_options

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
