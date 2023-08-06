from . import objects_pb2 as _objects_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateTaskReply(_message.Message):
    __slots__ = ["communication_token", "creation_status_list", "error"]
    class CreationStatus(_message.Message):
        __slots__ = ["error", "task_info"]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        TASK_INFO_FIELD_NUMBER: _ClassVar[int]
        error: str
        task_info: CreateTaskReply.TaskInfo
        def __init__(self, task_info: _Optional[_Union[CreateTaskReply.TaskInfo, _Mapping]] = ..., error: _Optional[str] = ...) -> None: ...
    class CreationStatusList(_message.Message):
        __slots__ = ["creation_statuses"]
        CREATION_STATUSES_FIELD_NUMBER: _ClassVar[int]
        creation_statuses: _containers.RepeatedCompositeFieldContainer[CreateTaskReply.CreationStatus]
        def __init__(self, creation_statuses: _Optional[_Iterable[_Union[CreateTaskReply.CreationStatus, _Mapping]]] = ...) -> None: ...
    class TaskInfo(_message.Message):
        __slots__ = ["data_dependencies", "expected_output_keys", "task_id"]
        DATA_DEPENDENCIES_FIELD_NUMBER: _ClassVar[int]
        EXPECTED_OUTPUT_KEYS_FIELD_NUMBER: _ClassVar[int]
        TASK_ID_FIELD_NUMBER: _ClassVar[int]
        data_dependencies: _containers.RepeatedScalarFieldContainer[str]
        expected_output_keys: _containers.RepeatedScalarFieldContainer[str]
        task_id: str
        def __init__(self, task_id: _Optional[str] = ..., expected_output_keys: _Optional[_Iterable[str]] = ..., data_dependencies: _Optional[_Iterable[str]] = ...) -> None: ...
    COMMUNICATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CREATION_STATUS_LIST_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    communication_token: str
    creation_status_list: CreateTaskReply.CreationStatusList
    error: str
    def __init__(self, creation_status_list: _Optional[_Union[CreateTaskReply.CreationStatusList, _Mapping]] = ..., error: _Optional[str] = ..., communication_token: _Optional[str] = ...) -> None: ...

class CreateTaskRequest(_message.Message):
    __slots__ = ["communication_token", "init_request", "init_task", "task_payload"]
    class InitRequest(_message.Message):
        __slots__ = ["task_options"]
        TASK_OPTIONS_FIELD_NUMBER: _ClassVar[int]
        task_options: _objects_pb2.TaskOptions
        def __init__(self, task_options: _Optional[_Union[_objects_pb2.TaskOptions, _Mapping]] = ...) -> None: ...
    COMMUNICATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    INIT_REQUEST_FIELD_NUMBER: _ClassVar[int]
    INIT_TASK_FIELD_NUMBER: _ClassVar[int]
    TASK_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    communication_token: str
    init_request: CreateTaskRequest.InitRequest
    init_task: _objects_pb2.InitTaskRequest
    task_payload: _objects_pb2.DataChunk
    def __init__(self, init_request: _Optional[_Union[CreateTaskRequest.InitRequest, _Mapping]] = ..., init_task: _Optional[_Union[_objects_pb2.InitTaskRequest, _Mapping]] = ..., task_payload: _Optional[_Union[_objects_pb2.DataChunk, _Mapping]] = ..., communication_token: _Optional[str] = ...) -> None: ...

class DataReply(_message.Message):
    __slots__ = ["communication_token", "data", "error", "init"]
    class Init(_message.Message):
        __slots__ = ["data", "error", "key"]
        DATA_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        KEY_FIELD_NUMBER: _ClassVar[int]
        data: _objects_pb2.DataChunk
        error: str
        key: str
        def __init__(self, key: _Optional[str] = ..., data: _Optional[_Union[_objects_pb2.DataChunk, _Mapping]] = ..., error: _Optional[str] = ...) -> None: ...
    COMMUNICATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    INIT_FIELD_NUMBER: _ClassVar[int]
    communication_token: str
    data: _objects_pb2.DataChunk
    error: str
    init: DataReply.Init
    def __init__(self, communication_token: _Optional[str] = ..., init: _Optional[_Union[DataReply.Init, _Mapping]] = ..., data: _Optional[_Union[_objects_pb2.DataChunk, _Mapping]] = ..., error: _Optional[str] = ...) -> None: ...

class DataRequest(_message.Message):
    __slots__ = ["communication_token", "key"]
    COMMUNICATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    communication_token: str
    key: str
    def __init__(self, communication_token: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class Result(_message.Message):
    __slots__ = ["communication_token", "data", "init"]
    COMMUNICATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    INIT_FIELD_NUMBER: _ClassVar[int]
    communication_token: str
    data: _objects_pb2.DataChunk
    init: _objects_pb2.InitKeyedDataStream
    def __init__(self, init: _Optional[_Union[_objects_pb2.InitKeyedDataStream, _Mapping]] = ..., data: _Optional[_Union[_objects_pb2.DataChunk, _Mapping]] = ..., communication_token: _Optional[str] = ...) -> None: ...

class ResultReply(_message.Message):
    __slots__ = ["Error", "Ok", "communication_token"]
    COMMUNICATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    Error: str
    OK_FIELD_NUMBER: _ClassVar[int]
    Ok: _objects_pb2.Empty
    communication_token: str
    def __init__(self, communication_token: _Optional[str] = ..., Ok: _Optional[_Union[_objects_pb2.Empty, _Mapping]] = ..., Error: _Optional[str] = ...) -> None: ...
