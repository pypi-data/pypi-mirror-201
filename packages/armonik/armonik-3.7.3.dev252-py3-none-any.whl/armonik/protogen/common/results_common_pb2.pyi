from google.protobuf import timestamp_pb2 as _timestamp_pb2
from . import result_status_pb2 as _result_status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetOwnerTaskIdRequest(_message.Message):
    __slots__ = ["result_id", "session_id"]
    RESULT_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    result_id: _containers.RepeatedScalarFieldContainer[str]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ..., result_id: _Optional[_Iterable[str]] = ...) -> None: ...

class GetOwnerTaskIdResponse(_message.Message):
    __slots__ = ["result_task", "session_id"]
    class MapResultTask(_message.Message):
        __slots__ = ["result_id", "task_id"]
        RESULT_ID_FIELD_NUMBER: _ClassVar[int]
        TASK_ID_FIELD_NUMBER: _ClassVar[int]
        result_id: str
        task_id: str
        def __init__(self, result_id: _Optional[str] = ..., task_id: _Optional[str] = ...) -> None: ...
    RESULT_TASK_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    result_task: _containers.RepeatedCompositeFieldContainer[GetOwnerTaskIdResponse.MapResultTask]
    session_id: str
    def __init__(self, result_task: _Optional[_Iterable[_Union[GetOwnerTaskIdResponse.MapResultTask, _Mapping]]] = ..., session_id: _Optional[str] = ...) -> None: ...

class ListResultsRequest(_message.Message):
    __slots__ = ["filter", "page", "page_size", "sort"]
    class OrderByField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class OrderDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Filter(_message.Message):
        __slots__ = ["created_after", "created_before", "name", "owner_task_id", "session_id", "status"]
        CREATED_AFTER_FIELD_NUMBER: _ClassVar[int]
        CREATED_BEFORE_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        OWNER_TASK_ID_FIELD_NUMBER: _ClassVar[int]
        SESSION_ID_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        created_after: _timestamp_pb2.Timestamp
        created_before: _timestamp_pb2.Timestamp
        name: str
        owner_task_id: str
        session_id: str
        status: _result_status_pb2.ResultStatus
        def __init__(self, session_id: _Optional[str] = ..., name: _Optional[str] = ..., owner_task_id: _Optional[str] = ..., status: _Optional[_Union[_result_status_pb2.ResultStatus, str]] = ..., created_after: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_before: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    class Sort(_message.Message):
        __slots__ = ["direction", "field"]
        DIRECTION_FIELD_NUMBER: _ClassVar[int]
        FIELD_FIELD_NUMBER: _ClassVar[int]
        direction: ListResultsRequest.OrderDirection
        field: ListResultsRequest.OrderByField
        def __init__(self, field: _Optional[_Union[ListResultsRequest.OrderByField, str]] = ..., direction: _Optional[_Union[ListResultsRequest.OrderDirection, str]] = ...) -> None: ...
    FILTER_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_CREATED_AT: ListResultsRequest.OrderByField
    ORDER_BY_FIELD_NAME: ListResultsRequest.OrderByField
    ORDER_BY_FIELD_OWNER_TASK_ID: ListResultsRequest.OrderByField
    ORDER_BY_FIELD_SESSION_ID: ListResultsRequest.OrderByField
    ORDER_BY_FIELD_STATUS: ListResultsRequest.OrderByField
    ORDER_BY_FIELD_UNSPECIFIED: ListResultsRequest.OrderByField
    ORDER_DIRECTION_ASC: ListResultsRequest.OrderDirection
    ORDER_DIRECTION_DESC: ListResultsRequest.OrderDirection
    ORDER_DIRECTION_UNSPECIFIED: ListResultsRequest.OrderDirection
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    filter: ListResultsRequest.Filter
    page: int
    page_size: int
    sort: ListResultsRequest.Sort
    def __init__(self, page: _Optional[int] = ..., page_size: _Optional[int] = ..., filter: _Optional[_Union[ListResultsRequest.Filter, _Mapping]] = ..., sort: _Optional[_Union[ListResultsRequest.Sort, _Mapping]] = ...) -> None: ...

class ListResultsResponse(_message.Message):
    __slots__ = ["page", "page_size", "results", "total"]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    results: _containers.RepeatedCompositeFieldContainer[ResultRaw]
    total: int
    def __init__(self, results: _Optional[_Iterable[_Union[ResultRaw, _Mapping]]] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ..., total: _Optional[int] = ...) -> None: ...

class ResultRaw(_message.Message):
    __slots__ = ["created_at", "name", "owner_task_id", "session_id", "status"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OWNER_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    name: str
    owner_task_id: str
    session_id: str
    status: _result_status_pb2.ResultStatus
    def __init__(self, session_id: _Optional[str] = ..., name: _Optional[str] = ..., owner_task_id: _Optional[str] = ..., status: _Optional[_Union[_result_status_pb2.ResultStatus, str]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
