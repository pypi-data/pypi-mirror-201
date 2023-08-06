from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedTokenUpdatePermissions")


@attr.s(auto_attribs=True)
class PatchedTokenUpdatePermissions:
    """Indicates per operation which permissions the database token has within the whole workspace. If the value of for
    example `create` is `true`, then the token can create rows in all tables related to the workspace. If a list is
    provided with for example `[["table", 1]]` then the token only has create permissions for the table with id 1. Same
    goes for if a database references is provided. `[['database', 1]]` means create permissions for all tables in the
    database with id 1.

    Example:
    ```json
    {
      "create": true// Allows creating rows in all tables.
      // Allows reading rows from database 1 and table 10.
      "read": [["database", 1], ["table", 10]],
      "update": false  // Denies updating rows in all tables.
      "delete": []  // Denies deleting rows in all tables.
     }
    ```

        Attributes:
            create (Union[List[List[Union[float, str]]], Unset, bool]):
            read (Union[List[List[Union[float, str]]], Unset, bool]):
            update (Union[List[List[Union[float, str]]], Unset, bool]):
            delete (Union[List[List[Union[float, str]]], Unset, bool]):
    """

    create: Union[List[List[Union[float, str]]], Unset, bool] = UNSET
    read: Union[List[List[Union[float, str]]], Unset, bool] = UNSET
    update: Union[List[List[Union[float, str]]], Unset, bool] = UNSET
    delete: Union[List[List[Union[float, str]]], Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        create: Union[List[List[Union[float, str]]], Unset, bool]
        if isinstance(self.create, Unset):
            create = UNSET

        elif isinstance(self.create, list):
            create = UNSET
            if not isinstance(self.create, Unset):
                create = []
                for create_type_1_item_data in self.create:
                    create_type_1_item = []
                    for create_type_1_item_item_data in create_type_1_item_data:
                        create_type_1_item_item: Union[float, str]

                        create_type_1_item_item = create_type_1_item_item_data

                        create_type_1_item.append(create_type_1_item_item)

                    create.append(create_type_1_item)

        else:
            create = self.create

        read: Union[List[List[Union[float, str]]], Unset, bool]
        if isinstance(self.read, Unset):
            read = UNSET

        elif isinstance(self.read, list):
            read = UNSET
            if not isinstance(self.read, Unset):
                read = []
                for read_type_1_item_data in self.read:
                    read_type_1_item = []
                    for read_type_1_item_item_data in read_type_1_item_data:
                        read_type_1_item_item: Union[float, str]

                        read_type_1_item_item = read_type_1_item_item_data

                        read_type_1_item.append(read_type_1_item_item)

                    read.append(read_type_1_item)

        else:
            read = self.read

        update: Union[List[List[Union[float, str]]], Unset, bool]
        if isinstance(self.update, Unset):
            update = UNSET

        elif isinstance(self.update, list):
            update = UNSET
            if not isinstance(self.update, Unset):
                update = []
                for update_type_1_item_data in self.update:
                    update_type_1_item = []
                    for update_type_1_item_item_data in update_type_1_item_data:
                        update_type_1_item_item: Union[float, str]

                        update_type_1_item_item = update_type_1_item_item_data

                        update_type_1_item.append(update_type_1_item_item)

                    update.append(update_type_1_item)

        else:
            update = self.update

        delete: Union[List[List[Union[float, str]]], Unset, bool]
        if isinstance(self.delete, Unset):
            delete = UNSET

        elif isinstance(self.delete, list):
            delete = UNSET
            if not isinstance(self.delete, Unset):
                delete = []
                for delete_type_1_item_data in self.delete:
                    delete_type_1_item = []
                    for delete_type_1_item_item_data in delete_type_1_item_data:
                        delete_type_1_item_item: Union[float, str]

                        delete_type_1_item_item = delete_type_1_item_item_data

                        delete_type_1_item.append(delete_type_1_item_item)

                    delete.append(delete_type_1_item)

        else:
            delete = self.delete

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if create is not UNSET:
            field_dict["create"] = create
        if read is not UNSET:
            field_dict["read"] = read
        if update is not UNSET:
            field_dict["update"] = update
        if delete is not UNSET:
            field_dict["delete"] = delete

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_create(data: object) -> Union[List[List[Union[float, str]]], Unset, bool]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                create_type_1 = UNSET
                _create_type_1 = data
                for create_type_1_item_data in _create_type_1 or []:
                    create_type_1_item = []
                    _create_type_1_item = create_type_1_item_data
                    for create_type_1_item_item_data in _create_type_1_item:

                        def _parse_create_type_1_item_item(data: object) -> Union[float, str]:
                            return cast(Union[float, str], data)

                        create_type_1_item_item = _parse_create_type_1_item_item(create_type_1_item_item_data)

                        create_type_1_item.append(create_type_1_item_item)

                    create_type_1.append(create_type_1_item)

                return create_type_1
            except:  # noqa: E722
                pass
            return cast(Union[List[List[Union[float, str]]], Unset, bool], data)

        create = _parse_create(d.pop("create", UNSET))

        def _parse_read(data: object) -> Union[List[List[Union[float, str]]], Unset, bool]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                read_type_1 = UNSET
                _read_type_1 = data
                for read_type_1_item_data in _read_type_1 or []:
                    read_type_1_item = []
                    _read_type_1_item = read_type_1_item_data
                    for read_type_1_item_item_data in _read_type_1_item:

                        def _parse_read_type_1_item_item(data: object) -> Union[float, str]:
                            return cast(Union[float, str], data)

                        read_type_1_item_item = _parse_read_type_1_item_item(read_type_1_item_item_data)

                        read_type_1_item.append(read_type_1_item_item)

                    read_type_1.append(read_type_1_item)

                return read_type_1
            except:  # noqa: E722
                pass
            return cast(Union[List[List[Union[float, str]]], Unset, bool], data)

        read = _parse_read(d.pop("read", UNSET))

        def _parse_update(data: object) -> Union[List[List[Union[float, str]]], Unset, bool]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                update_type_1 = UNSET
                _update_type_1 = data
                for update_type_1_item_data in _update_type_1 or []:
                    update_type_1_item = []
                    _update_type_1_item = update_type_1_item_data
                    for update_type_1_item_item_data in _update_type_1_item:

                        def _parse_update_type_1_item_item(data: object) -> Union[float, str]:
                            return cast(Union[float, str], data)

                        update_type_1_item_item = _parse_update_type_1_item_item(update_type_1_item_item_data)

                        update_type_1_item.append(update_type_1_item_item)

                    update_type_1.append(update_type_1_item)

                return update_type_1
            except:  # noqa: E722
                pass
            return cast(Union[List[List[Union[float, str]]], Unset, bool], data)

        update = _parse_update(d.pop("update", UNSET))

        def _parse_delete(data: object) -> Union[List[List[Union[float, str]]], Unset, bool]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                delete_type_1 = UNSET
                _delete_type_1 = data
                for delete_type_1_item_data in _delete_type_1 or []:
                    delete_type_1_item = []
                    _delete_type_1_item = delete_type_1_item_data
                    for delete_type_1_item_item_data in _delete_type_1_item:

                        def _parse_delete_type_1_item_item(data: object) -> Union[float, str]:
                            return cast(Union[float, str], data)

                        delete_type_1_item_item = _parse_delete_type_1_item_item(delete_type_1_item_item_data)

                        delete_type_1_item.append(delete_type_1_item_item)

                    delete_type_1.append(delete_type_1_item)

                return delete_type_1
            except:  # noqa: E722
                pass
            return cast(Union[List[List[Union[float, str]]], Unset, bool], data)

        delete = _parse_delete(d.pop("delete", UNSET))

        patched_token_update_permissions = cls(
            create=create,
            read=read,
            update=update,
            delete=delete,
        )

        patched_token_update_permissions.additional_properties = d
        return patched_token_update_permissions

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
