import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.sql_query_types_item import SqlQueryTypesItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.stream_column import StreamColumn


T = TypeVar("T", bound="SqlQuery")


@attr.s(auto_attribs=True)
class SqlQuery:
    """
    Attributes:
        parameters (List[str]):
        sql_query (Union[Unset, str]):
        start (Union[Unset, datetime.datetime]):
        end (Union[Unset, datetime.datetime]):
        limit (Union[Unset, float]):
        stream_columns (Union[Unset, List['StreamColumn']]):
        select_columns (Union[Unset, List[str]]):
        order_by_column (Union[Unset, str]):
        order_by_descending (Union[Unset, bool]):
        filters (Union[Unset, List[str]]):
        next_ (Union[Unset, float]):
        agent_ids (Union[Unset, List[str]]):
        device_ids (Union[Unset, List[str]]):
        names (Union[Unset, List[str]]):
        types (Union[Unset, List[SqlQueryTypesItem]]):
        tags (Union[Unset, Any]):
        not_names (Union[Unset, List[str]]):
    """

    parameters: List[str]
    sql_query: Union[Unset, str] = UNSET
    start: Union[Unset, datetime.datetime] = UNSET
    end: Union[Unset, datetime.datetime] = UNSET
    limit: Union[Unset, float] = UNSET
    stream_columns: Union[Unset, List["StreamColumn"]] = UNSET
    select_columns: Union[Unset, List[str]] = UNSET
    order_by_column: Union[Unset, str] = UNSET
    order_by_descending: Union[Unset, bool] = UNSET
    filters: Union[Unset, List[str]] = UNSET
    next_: Union[Unset, float] = UNSET
    agent_ids: Union[Unset, List[str]] = UNSET
    device_ids: Union[Unset, List[str]] = UNSET
    names: Union[Unset, List[str]] = UNSET
    types: Union[Unset, List[SqlQueryTypesItem]] = UNSET
    tags: Union[Unset, Any] = UNSET
    not_names: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        parameters = self.parameters

        sql_query = self.sql_query
        start: Union[Unset, str] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.isoformat()

        end: Union[Unset, str] = UNSET
        if not isinstance(self.end, Unset):
            end = self.end.isoformat()

        limit = self.limit
        stream_columns: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.stream_columns, Unset):
            stream_columns = []
            for stream_columns_item_data in self.stream_columns:
                stream_columns_item = stream_columns_item_data.to_dict()

                stream_columns.append(stream_columns_item)

        select_columns: Union[Unset, List[str]] = UNSET
        if not isinstance(self.select_columns, Unset):
            select_columns = self.select_columns

        order_by_column = self.order_by_column
        order_by_descending = self.order_by_descending
        filters: Union[Unset, List[str]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = self.filters

        next_ = self.next_
        agent_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.agent_ids, Unset):
            agent_ids = self.agent_ids

        device_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.device_ids, Unset):
            device_ids = self.device_ids

        names: Union[Unset, List[str]] = UNSET
        if not isinstance(self.names, Unset):
            names = self.names

        types: Union[Unset, List[str]] = UNSET
        if not isinstance(self.types, Unset):
            types = []
            for types_item_data in self.types:
                types_item = types_item_data.value

                types.append(types_item)

        tags = self.tags
        not_names: Union[Unset, List[str]] = UNSET
        if not isinstance(self.not_names, Unset):
            not_names = self.not_names

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "parameters": parameters,
            }
        )
        if sql_query is not UNSET:
            field_dict["sqlQuery"] = sql_query
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if limit is not UNSET:
            field_dict["limit"] = limit
        if stream_columns is not UNSET:
            field_dict["streamColumns"] = stream_columns
        if select_columns is not UNSET:
            field_dict["selectColumns"] = select_columns
        if order_by_column is not UNSET:
            field_dict["orderByColumn"] = order_by_column
        if order_by_descending is not UNSET:
            field_dict["orderByDescending"] = order_by_descending
        if filters is not UNSET:
            field_dict["filters"] = filters
        if next_ is not UNSET:
            field_dict["next"] = next_
        if agent_ids is not UNSET:
            field_dict["agentIds"] = agent_ids
        if device_ids is not UNSET:
            field_dict["deviceIds"] = device_ids
        if names is not UNSET:
            field_dict["names"] = names
        if types is not UNSET:
            field_dict["types"] = types
        if tags is not UNSET:
            field_dict["tags"] = tags
        if not_names is not UNSET:
            field_dict["notNames"] = not_names

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.stream_column import StreamColumn

        d = src_dict.copy()
        parameters = cast(List[str], d.pop("parameters"))

        sql_query = d.pop("sqlQuery", UNSET)

        _start = d.pop("start", UNSET)
        start: Union[Unset, datetime.datetime]
        if isinstance(_start, Unset):
            start = UNSET
        else:
            start = isoparse(_start)

        _end = d.pop("end", UNSET)
        end: Union[Unset, datetime.datetime]
        if isinstance(_end, Unset):
            end = UNSET
        else:
            end = isoparse(_end)

        limit = d.pop("limit", UNSET)

        stream_columns = []
        _stream_columns = d.pop("streamColumns", UNSET)
        for stream_columns_item_data in _stream_columns or []:
            stream_columns_item = StreamColumn.from_dict(stream_columns_item_data)

            stream_columns.append(stream_columns_item)

        select_columns = cast(List[str], d.pop("selectColumns", UNSET))

        order_by_column = d.pop("orderByColumn", UNSET)

        order_by_descending = d.pop("orderByDescending", UNSET)

        filters = cast(List[str], d.pop("filters", UNSET))

        next_ = d.pop("next", UNSET)

        agent_ids = cast(List[str], d.pop("agentIds", UNSET))

        device_ids = cast(List[str], d.pop("deviceIds", UNSET))

        names = cast(List[str], d.pop("names", UNSET))

        types = []
        _types = d.pop("types", UNSET)
        for types_item_data in _types or []:
            types_item = SqlQueryTypesItem(types_item_data)

            types.append(types_item)

        tags = d.pop("tags", UNSET)

        not_names = cast(List[str], d.pop("notNames", UNSET))

        sql_query = cls(
            parameters=parameters,
            sql_query=sql_query,
            start=start,
            end=end,
            limit=limit,
            stream_columns=stream_columns,
            select_columns=select_columns,
            order_by_column=order_by_column,
            order_by_descending=order_by_descending,
            filters=filters,
            next_=next_,
            agent_ids=agent_ids,
            device_ids=device_ids,
            names=names,
            types=types,
            tags=tags,
            not_names=not_names,
        )

        sql_query.additional_properties = d
        return sql_query

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
