import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_user_request_tags import CreateUserRequestTags


T = TypeVar("T", bound="CreateUserRequest")


@attr.s(auto_attribs=True)
class CreateUserRequest:
    """
    Attributes:
        email (str):
        first_name (str):
        role_id (str):
        password (Union[Unset, str]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        tags (Union[Unset, CreateUserRequestTags]):
        organization_id (Union[Unset, str]):
        last_name (Union[Unset, str]):
        team_id (Union[Unset, None, str]):
        phone_number (Union[Unset, str]):
        enabled (Union[Unset, bool]):
        is_organization_owner (Union[Unset, bool]):
        terms_accepted (Union[Unset, str]):
        last_logged_in (Union[Unset, datetime.datetime]):
        password_hash (Union[Unset, None, str]):
        is_single_sign_on (Union[Unset, bool]):
        is_service_account (Union[Unset, bool]):
    """

    email: str
    first_name: str
    role_id: str
    password: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    tags: Union[Unset, "CreateUserRequestTags"] = UNSET
    organization_id: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    team_id: Union[Unset, None, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    is_organization_owner: Union[Unset, bool] = UNSET
    terms_accepted: Union[Unset, str] = UNSET
    last_logged_in: Union[Unset, datetime.datetime] = UNSET
    password_hash: Union[Unset, None, str] = UNSET
    is_single_sign_on: Union[Unset, bool] = UNSET
    is_service_account: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        first_name = self.first_name
        role_id = self.role_id
        password = self.password
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        organization_id = self.organization_id
        last_name = self.last_name
        team_id = self.team_id
        phone_number = self.phone_number
        enabled = self.enabled
        is_organization_owner = self.is_organization_owner
        terms_accepted = self.terms_accepted
        last_logged_in: Union[Unset, str] = UNSET
        if not isinstance(self.last_logged_in, Unset):
            last_logged_in = self.last_logged_in.isoformat()

        password_hash = self.password_hash
        is_single_sign_on = self.is_single_sign_on
        is_service_account = self.is_service_account

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "firstName": first_name,
                "roleId": role_id,
            }
        )
        if password is not UNSET:
            field_dict["password"] = password
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if tags is not UNSET:
            field_dict["tags"] = tags
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if team_id is not UNSET:
            field_dict["teamId"] = team_id
        if phone_number is not UNSET:
            field_dict["phoneNumber"] = phone_number
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if is_organization_owner is not UNSET:
            field_dict["isOrganizationOwner"] = is_organization_owner
        if terms_accepted is not UNSET:
            field_dict["termsAccepted"] = terms_accepted
        if last_logged_in is not UNSET:
            field_dict["lastLoggedIn"] = last_logged_in
        if password_hash is not UNSET:
            field_dict["passwordHash"] = password_hash
        if is_single_sign_on is not UNSET:
            field_dict["isSingleSignOn"] = is_single_sign_on
        if is_service_account is not UNSET:
            field_dict["isServiceAccount"] = is_service_account

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_user_request_tags import CreateUserRequestTags

        d = src_dict.copy()
        email = d.pop("email")

        first_name = d.pop("firstName")

        role_id = d.pop("roleId")

        password = d.pop("password", UNSET)

        id = d.pop("id", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, CreateUserRequestTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = CreateUserRequestTags.from_dict(_tags)

        organization_id = d.pop("organizationId", UNSET)

        last_name = d.pop("lastName", UNSET)

        team_id = d.pop("teamId", UNSET)

        phone_number = d.pop("phoneNumber", UNSET)

        enabled = d.pop("enabled", UNSET)

        is_organization_owner = d.pop("isOrganizationOwner", UNSET)

        terms_accepted = d.pop("termsAccepted", UNSET)

        _last_logged_in = d.pop("lastLoggedIn", UNSET)
        last_logged_in: Union[Unset, datetime.datetime]
        if isinstance(_last_logged_in, Unset):
            last_logged_in = UNSET
        else:
            last_logged_in = isoparse(_last_logged_in)

        password_hash = d.pop("passwordHash", UNSET)

        is_single_sign_on = d.pop("isSingleSignOn", UNSET)

        is_service_account = d.pop("isServiceAccount", UNSET)

        create_user_request = cls(
            email=email,
            first_name=first_name,
            role_id=role_id,
            password=password,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            tags=tags,
            organization_id=organization_id,
            last_name=last_name,
            team_id=team_id,
            phone_number=phone_number,
            enabled=enabled,
            is_organization_owner=is_organization_owner,
            terms_accepted=terms_accepted,
            last_logged_in=last_logged_in,
            password_hash=password_hash,
            is_single_sign_on=is_single_sign_on,
            is_service_account=is_service_account,
        )

        create_user_request.additional_properties = d
        return create_user_request

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
