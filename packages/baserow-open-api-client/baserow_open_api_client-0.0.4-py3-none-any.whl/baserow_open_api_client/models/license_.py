import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="License")


@attr.s(auto_attribs=True)
class License:
    """
    Attributes:
        id (int):
        license_id (str): Unique identifier of the license.
        is_active (bool): Indicates if the backend deems the license valid.
        valid_from (datetime.datetime): From which timestamp the license becomes active.
        valid_through (datetime.datetime): Until which timestamp the license is active.
        free_users_count (int): The amount of free users that are currently using the license.
        seats_taken (int): The amount of users that are currently using the license.
        seats (int): The maximum amount of users that can use the license.
        product_code (str): The product code that indicates what the license unlocks.
        issued_on (datetime.datetime): The date when the license was issued. It could be that a new license is issued
            with the same `license_id` because it was updated. In that case, the one that has been issued last should be
            used.
        issued_to_email (str): Indicates to which email address the license has been issued.
        issued_to_name (str): Indicates to whom the license has been issued.
        last_check (Union[Unset, None, datetime.datetime]):
    """

    id: int
    license_id: str
    is_active: bool
    valid_from: datetime.datetime
    valid_through: datetime.datetime
    free_users_count: int
    seats_taken: int
    seats: int
    product_code: str
    issued_on: datetime.datetime
    issued_to_email: str
    issued_to_name: str
    last_check: Union[Unset, None, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        license_id = self.license_id
        is_active = self.is_active
        valid_from = self.valid_from.isoformat()

        valid_through = self.valid_through.isoformat()

        free_users_count = self.free_users_count
        seats_taken = self.seats_taken
        seats = self.seats
        product_code = self.product_code
        issued_on = self.issued_on.isoformat()

        issued_to_email = self.issued_to_email
        issued_to_name = self.issued_to_name
        last_check: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_check, Unset):
            last_check = self.last_check.isoformat() if self.last_check else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "license_id": license_id,
                "is_active": is_active,
                "valid_from": valid_from,
                "valid_through": valid_through,
                "free_users_count": free_users_count,
                "seats_taken": seats_taken,
                "seats": seats,
                "product_code": product_code,
                "issued_on": issued_on,
                "issued_to_email": issued_to_email,
                "issued_to_name": issued_to_name,
            }
        )
        if last_check is not UNSET:
            field_dict["last_check"] = last_check

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        license_id = d.pop("license_id")

        is_active = d.pop("is_active")

        valid_from = isoparse(d.pop("valid_from"))

        valid_through = isoparse(d.pop("valid_through"))

        free_users_count = d.pop("free_users_count")

        seats_taken = d.pop("seats_taken")

        seats = d.pop("seats")

        product_code = d.pop("product_code")

        issued_on = isoparse(d.pop("issued_on"))

        issued_to_email = d.pop("issued_to_email")

        issued_to_name = d.pop("issued_to_name")

        _last_check = d.pop("last_check", UNSET)
        last_check: Union[Unset, None, datetime.datetime]
        if _last_check is None:
            last_check = None
        elif isinstance(_last_check, Unset):
            last_check = UNSET
        else:
            last_check = isoparse(_last_check)

        license_ = cls(
            id=id,
            license_id=license_id,
            is_active=is_active,
            valid_from=valid_from,
            valid_through=valid_through,
            free_users_count=free_users_count,
            seats_taken=seats_taken,
            seats=seats,
            product_code=product_code,
            issued_on=issued_on,
            issued_to_email=issued_to_email,
            issued_to_name=issued_to_name,
            last_check=last_check,
        )

        license_.additional_properties = d
        return license_

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
