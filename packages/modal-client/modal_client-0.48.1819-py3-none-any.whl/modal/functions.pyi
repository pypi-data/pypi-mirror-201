import __main__
import google.protobuf.message
import modal._function_utils
import modal._output
import modal._resolver
import modal.call_graph
import modal.client
import modal.gpu
import modal.image
import modal.mount
import modal.object
import modal.proxy
import modal.retries
import modal.schedule
import modal.secret
import modal.shared_volume
import modal.stub
import modal_proto.api_pb2
import typing

def exc_with_hints(exc: BaseException):
    ...


async def _process_result(result, stub, client=None):
    ...


async def _create_input(args, kwargs, client, idx=None) -> modal_proto.api_pb2.FunctionPutInputsItem:
    ...


class _OutputValue:
    value: typing.Any

    def __init__(self, value: typing.Any) -> None:
        ...

    def __repr__(self):
        ...

    def __eq__(self, other):
        ...


class _Invocation:
    def __init__(self, stub, function_call_id, client=None):
        ...

    @staticmethod
    async def create(function_id, args, kwargs, client):
        ...

    def pop_function_call_outputs(self, timeout: typing.Union[float, None], clear_on_success: bool):
        ...

    async def run_function(self):
        ...

    async def poll_function(self, timeout: typing.Union[float, None] = None):
        ...

    def run_generator(self):
        ...


def _map_invocation(function_id: str, input_stream: typing.AsyncIterable[typing.Any], kwargs: typing.Dict[str, typing.Any], client: modal.client._Client, is_generator: bool, order_outputs: bool, return_exceptions: bool, count_update_callback: typing.Union[typing.Callable[[int, int], None], None]):
    ...


class FunctionStats:
    backlog: int
    num_active_runners: int
    num_total_runners: int

    def __init__(self, backlog: int, num_active_runners: int, num_total_runners: int) -> None:
        ...

    def __repr__(self):
        ...

    def __eq__(self, other):
        ...


class _FunctionHandle(modal.object._Handle):
    _web_url: typing.Union[str, None]
    _info: typing.Union[modal._function_utils.FunctionInfo, None]
    _stub: typing.Union[modal.stub._Stub, None]

    def _initialize_from_empty(self):
        ...

    def _initialize_from_proto(self, proto: google.protobuf.message.Message):
        ...

    def _initialize_from_local(self, stub, info: modal._function_utils.FunctionInfo):
        ...

    def _set_mute_cancellation(self, value: bool = True):
        ...

    def _set_output_mgr(self, output_mgr: modal._output.OutputManager):
        ...

    def _get_function(self) -> _Function:
        ...

    @property
    def web_url(self) -> str:
        ...

    @property
    def is_generator(self) -> bool:
        ...

    def _map(self, input_stream: typing.AsyncIterable[typing.Any], order_outputs: bool, return_exceptions: bool, kwargs={}):
        ...

    def map(self, *input_iterators, kwargs={}, order_outputs=None, return_exceptions=False):
        ...

    async def for_each(self, *input_iterators, kwargs={}, ignore_exceptions=False):
        ...

    def starmap(self, input_iterator, kwargs={}, order_outputs=None, return_exceptions=False):
        ...

    async def call_function(self, args, kwargs):
        ...

    async def call_function_nowait(self, args, kwargs):
        ...

    def call_generator(self, args, kwargs):
        ...

    async def _call_generator_nowait(self, args, kwargs):
        ...

    def call(self, *args, **kwargs) -> typing.Any:
        ...

    def __call__(self, *args, **kwargs) -> typing.Any:
        ...

    async def spawn(self, *args, **kwargs) -> typing.Union[_FunctionCall, None]:
        ...

    def get_raw_f(self) -> typing.Callable[..., typing.Any]:
        ...

    async def get_current_stats(self) -> FunctionStats:
        ...

    def __get__(self, obj, objtype=None) -> _FunctionHandle:
        ...


class FunctionHandle(modal.object.Handle):
    _web_url: typing.Union[str, None]
    _info: typing.Union[modal._function_utils.FunctionInfo, None]
    _stub: typing.Union[modal.stub.Stub, None]

    def __init__(self):
        ...

    def _initialize_from_empty(self):
        ...

    def _initialize_from_proto(self, proto: google.protobuf.message.Message):
        ...

    def _initialize_from_local(self, stub, info: modal._function_utils.FunctionInfo):
        ...

    def _set_mute_cancellation(self, value: bool = True):
        ...

    def _set_output_mgr(self, output_mgr: modal._output.OutputManager):
        ...

    def _get_function(self) -> Function:
        ...

    @property
    def web_url(self) -> str:
        ...

    @property
    def is_generator(self) -> bool:
        ...

    def _map(self, input_stream: typing.Iterable[typing.Any], order_outputs: bool, return_exceptions: bool, kwargs={}):
        ...

    def map(self, *input_iterators, kwargs={}, order_outputs=None, return_exceptions=False):
        ...

    def for_each(self, *input_iterators, kwargs={}, ignore_exceptions=False):
        ...

    def starmap(self, input_iterator, kwargs={}, order_outputs=None, return_exceptions=False):
        ...

    def call_function(self, args, kwargs):
        ...

    def call_function_nowait(self, args, kwargs):
        ...

    def call_generator(self, args, kwargs):
        ...

    def _call_generator_nowait(self, args, kwargs):
        ...

    def call(self, *args, **kwargs) -> typing.Any:
        ...

    def __call__(self, *args, **kwargs) -> typing.Any:
        ...

    def spawn(self, *args, **kwargs) -> typing.Union[FunctionCall, None]:
        ...

    def get_raw_f(self) -> typing.Callable[..., typing.Any]:
        ...

    def get_current_stats(self) -> FunctionStats:
        ...

    def __get__(self, obj, objtype=None) -> FunctionHandle:
        ...


class AioFunctionHandle(modal.object.AioHandle):
    _web_url: typing.Union[str, None]
    _info: typing.Union[modal._function_utils.FunctionInfo, None]
    _stub: typing.Union[modal.stub.AioStub, None]

    def __init__(self):
        ...

    def _initialize_from_empty(self):
        ...

    def _initialize_from_proto(self, proto: google.protobuf.message.Message):
        ...

    def _initialize_from_local(self, stub, info: modal._function_utils.FunctionInfo):
        ...

    def _set_mute_cancellation(self, value: bool = True):
        ...

    def _set_output_mgr(self, output_mgr: modal._output.OutputManager):
        ...

    def _get_function(self) -> AioFunction:
        ...

    @property
    def web_url(self) -> str:
        ...

    @property
    def is_generator(self) -> bool:
        ...

    def _map(self, input_stream: typing.AsyncIterable[typing.Any], order_outputs: bool, return_exceptions: bool, kwargs={}):
        ...

    def map(self, *input_iterators, kwargs={}, order_outputs=None, return_exceptions=False):
        ...

    async def for_each(self, *args, **kwargs):
        ...

    def starmap(self, input_iterator, kwargs={}, order_outputs=None, return_exceptions=False):
        ...

    async def call_function(self, *args, **kwargs):
        ...

    async def call_function_nowait(self, *args, **kwargs):
        ...

    def call_generator(self, args, kwargs):
        ...

    async def _call_generator_nowait(self, *args, **kwargs):
        ...

    def call(self, *args, **kwargs) -> typing.Any:
        ...

    def __call__(self, *args, **kwargs) -> typing.Any:
        ...

    async def spawn(self, *args, **kwargs) -> typing.Union[AioFunctionCall, None]:
        ...

    def get_raw_f(self) -> typing.Callable[..., typing.Any]:
        ...

    async def get_current_stats(self, *args, **kwargs) -> FunctionStats:
        ...

    def __get__(self, obj, objtype=None) -> AioFunctionHandle:
        ...


class _Function(modal.object._Provider[_FunctionHandle]):
    _secrets: typing.Collection[modal.secret._Secret]
    _info: modal._function_utils.FunctionInfo
    _mounts: typing.Collection[modal.mount._Mount]
    _shared_volumes: typing.Dict[str, modal.shared_volume._SharedVolume]
    _allow_cross_region_volumes: bool
    _image: typing.Union[modal.image._Image, None]
    _gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig]
    _cloud: typing.Union[str, None]
    _function_handle: _FunctionHandle
    _stub: modal.stub._Stub

    def __init__(self, function_handle: _FunctionHandle, function_info: modal._function_utils.FunctionInfo, _stub, image=None, secret: typing.Union[modal.secret._Secret, None] = None, secrets: typing.Collection[modal.secret._Secret] = (), schedule: typing.Union[modal.schedule.Schedule, None] = None, is_generator=False, gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, serialized: bool = False, base_mounts: typing.Collection[modal.mount._Mount] = (), mounts: typing.Collection[modal.mount._Mount] = (), shared_volumes: typing.Dict[str, modal.shared_volume._SharedVolume] = {}, allow_cross_region_volumes: bool = False, webhook_config: typing.Union[modal_proto.api_pb2.WebhookConfig, None] = None, memory: typing.Union[int, None] = None, proxy: typing.Union[modal.proxy._Proxy, None] = None, retries: typing.Union[int, modal.retries.Retries, None] = None, timeout: typing.Union[int, None] = None, concurrency_limit: typing.Union[int, None] = None, container_idle_timeout: typing.Union[int, None] = None, cpu: typing.Union[float, None] = None, keep_warm: typing.Union[bool, int, None] = None, interactive: bool = False, name: typing.Union[str, None] = None, cloud: typing.Union[str, None] = None) -> None:
        ...

    async def _load(self, resolver: modal._resolver.Resolver, existing_object_id: str):
        ...

    def get_panel_items(self) -> typing.List[str]:
        ...

    @property
    def tag(self):
        ...

    def get_build_def(self):
        ...


class Function(modal.object.Provider[FunctionHandle]):
    _secrets: typing.Collection[modal.secret.Secret]
    _info: modal._function_utils.FunctionInfo
    _mounts: typing.Collection[modal.mount.Mount]
    _shared_volumes: typing.Dict[str, modal.shared_volume.SharedVolume]
    _allow_cross_region_volumes: bool
    _image: typing.Union[modal.image.Image, None]
    _gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig]
    _cloud: typing.Union[str, None]
    _function_handle: FunctionHandle
    _stub: modal.stub.Stub

    def __init__(self, function_handle: FunctionHandle, function_info: modal._function_utils.FunctionInfo, _stub, image=None, secret: typing.Union[modal.secret.Secret, None] = None, secrets: typing.Collection[modal.secret.Secret] = (), schedule: typing.Union[modal.schedule.Schedule, None] = None, is_generator=False, gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, serialized: bool = False, base_mounts: typing.Collection[modal.mount.Mount] = (), mounts: typing.Collection[modal.mount.Mount] = (), shared_volumes: typing.Dict[str, modal.shared_volume.SharedVolume] = {}, allow_cross_region_volumes: bool = False, webhook_config: typing.Union[modal_proto.api_pb2.WebhookConfig, None] = None, memory: typing.Union[int, None] = None, proxy: typing.Union[modal.proxy.Proxy, None] = None, retries: typing.Union[int, modal.retries.Retries, None] = None, timeout: typing.Union[int, None] = None, concurrency_limit: typing.Union[int, None] = None, container_idle_timeout: typing.Union[int, None] = None, cpu: typing.Union[float, None] = None, keep_warm: typing.Union[bool, int, None] = None, interactive: bool = False, name: typing.Union[str, None] = None, cloud: typing.Union[str, None] = None) -> None:
        ...

    def _load(self, resolver: modal._resolver.Resolver, existing_object_id: str):
        ...

    def get_panel_items(self) -> typing.List[str]:
        ...

    @property
    def tag(self):
        ...

    def get_build_def(self):
        ...


class AioFunction(modal.object.AioProvider[AioFunctionHandle]):
    _secrets: typing.Collection[modal.secret.AioSecret]
    _info: modal._function_utils.FunctionInfo
    _mounts: typing.Collection[modal.mount.AioMount]
    _shared_volumes: typing.Dict[str, modal.shared_volume.AioSharedVolume]
    _allow_cross_region_volumes: bool
    _image: typing.Union[modal.image.AioImage, None]
    _gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig]
    _cloud: typing.Union[str, None]
    _function_handle: AioFunctionHandle
    _stub: modal.stub.AioStub

    def __init__(self, function_handle: AioFunctionHandle, function_info: modal._function_utils.FunctionInfo, _stub, image=None, secret: typing.Union[modal.secret.AioSecret, None] = None, secrets: typing.Collection[modal.secret.AioSecret] = (), schedule: typing.Union[modal.schedule.Schedule, None] = None, is_generator=False, gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, serialized: bool = False, base_mounts: typing.Collection[modal.mount.AioMount] = (), mounts: typing.Collection[modal.mount.AioMount] = (), shared_volumes: typing.Dict[str, modal.shared_volume.AioSharedVolume] = {}, allow_cross_region_volumes: bool = False, webhook_config: typing.Union[modal_proto.api_pb2.WebhookConfig, None] = None, memory: typing.Union[int, None] = None, proxy: typing.Union[modal.proxy.AioProxy, None] = None, retries: typing.Union[int, modal.retries.Retries, None] = None, timeout: typing.Union[int, None] = None, concurrency_limit: typing.Union[int, None] = None, container_idle_timeout: typing.Union[int, None] = None, cpu: typing.Union[float, None] = None, keep_warm: typing.Union[bool, int, None] = None, interactive: bool = False, name: typing.Union[str, None] = None, cloud: typing.Union[str, None] = None) -> None:
        ...

    async def _load(self, *args, **kwargs):
        ...

    def get_panel_items(self) -> typing.List[str]:
        ...

    @property
    def tag(self):
        ...

    def get_build_def(self):
        ...


class _FunctionCall(modal.object._Handle):
    def _invocation(self):
        ...

    async def get(self, timeout: typing.Union[float, None] = None):
        ...

    async def get_call_graph(self) -> typing.List[modal.call_graph.InputInfo]:
        ...

    async def cancel(self):
        ...


class FunctionCall(modal.object.Handle):
    def __init__(self):
        ...

    def _invocation(self):
        ...

    def get(self, timeout: typing.Union[float, None] = None):
        ...

    def get_call_graph(self) -> typing.List[modal.call_graph.InputInfo]:
        ...

    def cancel(self):
        ...


class AioFunctionCall(modal.object.AioHandle):
    def __init__(self):
        ...

    def _invocation(self):
        ...

    async def get(self, *args, **kwargs):
        ...

    async def get_call_graph(self, *args, **kwargs) -> typing.List[modal.call_graph.InputInfo]:
        ...

    async def cancel(self, *args, **kwargs):
        ...


async def _gather(*function_calls: _FunctionCall):
    ...


def gather(*function_calls: FunctionCall):
    ...


async def aio_gather(*args, **kwargs):
    ...


def current_input_id() -> str:
    ...


def _set_current_input_id(input_id: typing.Union[str, None]):
    ...


_current_input_id: typing.Union[str, None]