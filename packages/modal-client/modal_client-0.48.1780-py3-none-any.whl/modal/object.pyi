import google.protobuf.message
import modal._resolver
import modal.client
import typing

H = typing.TypeVar("H", bound="_Handle")

_BLOCKING_H = typing.TypeVar("_BLOCKING_H", bound="Handle")

_ASYNC_H = typing.TypeVar("_ASYNC_H", bound="AioHandle")

class _Handle:
    _type_prefix: str

    def __init__(self):
        ...

    def _init(self):
        ...

    @classmethod
    def _new(cls: typing.Type[H]) -> H:
        ...

    def _initialize_handle(self, client: modal.client._Client, object_id: str):
        ...

    def _initialize_from_empty(self):
        ...

    def _initialize_from_proto(self, proto: google.protobuf.message.Message):
        ...

    @classmethod
    def _from_id(cls: typing.Type[H], object_id: str, client: modal.client._Client, proto: typing.Union[google.protobuf.message.Message, None]) -> H:
        ...

    @classmethod
    async def from_id(cls: typing.Type[H], object_id: str, client: typing.Union[modal.client._Client, None] = None) -> H:
        ...

    @property
    def object_id(self) -> str:
        ...

    @classmethod
    async def from_app(cls: typing.Type[H], app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client._Client, None] = None) -> H:
        ...


class Handle:
    _type_prefix: str

    def __init__(self):
        ...

    def _init(self):
        ...

    @classmethod
    def _new(cls: typing.Type[_BLOCKING_H]) -> _BLOCKING_H:
        ...

    def _initialize_handle(self, client: modal.client.Client, object_id: str):
        ...

    def _initialize_from_empty(self):
        ...

    def _initialize_from_proto(self, proto: google.protobuf.message.Message):
        ...

    @classmethod
    def _from_id(cls: typing.Type[_BLOCKING_H], object_id: str, client: modal.client.Client, proto: typing.Union[google.protobuf.message.Message, None]) -> _BLOCKING_H:
        ...

    @classmethod
    def from_id(cls: typing.Type[_BLOCKING_H], object_id: str, client: typing.Union[modal.client.Client, None] = None) -> _BLOCKING_H:
        ...

    @property
    def object_id(self) -> str:
        ...

    @classmethod
    def from_app(cls: typing.Type[_BLOCKING_H], app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client.Client, None] = None) -> _BLOCKING_H:
        ...


class AioHandle:
    _type_prefix: str

    def __init__(self):
        ...

    def _init(self):
        ...

    @classmethod
    def _new(cls: typing.Type[_ASYNC_H]) -> _ASYNC_H:
        ...

    def _initialize_handle(self, client: modal.client.AioClient, object_id: str):
        ...

    def _initialize_from_empty(self):
        ...

    def _initialize_from_proto(self, proto: google.protobuf.message.Message):
        ...

    @classmethod
    def _from_id(cls: typing.Type[_ASYNC_H], object_id: str, client: modal.client.AioClient, proto: typing.Union[google.protobuf.message.Message, None]) -> _ASYNC_H:
        ...

    @classmethod
    async def from_id(cls, *args, **kwargs) -> _ASYNC_H:
        ...

    @property
    def object_id(self) -> str:
        ...

    @classmethod
    async def from_app(cls, *args, **kwargs) -> _ASYNC_H:
        ...


async def _lookup(app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client._Client, None] = None) -> _Handle:
    ...


def lookup(app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client.Client, None] = None) -> Handle:
    ...


async def aio_lookup(*args, **kwargs) -> AioHandle:
    ...


P = typing.TypeVar("P", bound="_Provider")

_BLOCKING_P = typing.TypeVar("_BLOCKING_P", bound="Provider")

_ASYNC_P = typing.TypeVar("_ASYNC_P", bound="AioProvider")

class _Provider(typing.Generic[H]):
    def _init(self, load: typing.Callable[[modal._resolver.Resolver, str], typing.Awaitable[H]], rep: str):
        ...

    def __init__(self, load: typing.Callable[[modal._resolver.Resolver, str], typing.Awaitable[H]], rep: str):
        ...

    @classmethod
    def _from_loader(cls, load: typing.Callable[[modal._resolver.Resolver, str], typing.Awaitable[H]], rep: str):
        ...

    @classmethod
    def _get_handle_cls(cls):
        ...

    def __repr__(self):
        ...

    @property
    def local_uuid(self):
        ...

    async def _deploy(self, label: str, namespace=1, client: typing.Union[modal.client._Client, None] = None) -> H:
        ...

    def persist(self, label: str, namespace=1):
        ...

    @classmethod
    def from_name(cls: typing.Type[P], app_name: str, tag: typing.Union[str, None] = None, namespace=1) -> P:
        ...

    @classmethod
    async def lookup(cls: typing.Type[P], app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client._Client, None] = None) -> H:
        ...

    @classmethod
    async def _exists(cls: typing.Type[P], app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client._Client, None] = None) -> bool:
        ...


class Provider(typing.Generic[_BLOCKING_H]):
    def __init__(self, load: typing.Callable[[modal._resolver.Resolver, str], _BLOCKING_H], rep: str):
        ...

    def _init(self, load: typing.Callable[[modal._resolver.Resolver, str], _BLOCKING_H], rep: str):
        ...

    @classmethod
    def _from_loader(cls, load: typing.Callable[[modal._resolver.Resolver, str], _BLOCKING_H], rep: str):
        ...

    @classmethod
    def _get_handle_cls(cls):
        ...

    def __repr__(self):
        ...

    @property
    def local_uuid(self):
        ...

    def _deploy(self, label: str, namespace=1, client: typing.Union[modal.client.Client, None] = None) -> _BLOCKING_H:
        ...

    def persist(self, label: str, namespace=1):
        ...

    @classmethod
    def from_name(cls: typing.Type[_BLOCKING_P], app_name: str, tag: typing.Union[str, None] = None, namespace=1) -> _BLOCKING_P:
        ...

    @classmethod
    def lookup(cls: typing.Type[_BLOCKING_P], app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client.Client, None] = None) -> _BLOCKING_H:
        ...

    @classmethod
    def _exists(cls: typing.Type[_BLOCKING_P], app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client.Client, None] = None) -> bool:
        ...


class AioProvider(typing.Generic[_ASYNC_H]):
    def __init__(self, load: typing.Callable[[modal._resolver.Resolver, str], typing.Awaitable[_ASYNC_H]], rep: str):
        ...

    def _init(self, load: typing.Callable[[modal._resolver.Resolver, str], typing.Awaitable[_ASYNC_H]], rep: str):
        ...

    @classmethod
    def _from_loader(cls, load: typing.Callable[[modal._resolver.Resolver, str], typing.Awaitable[_ASYNC_H]], rep: str):
        ...

    @classmethod
    def _get_handle_cls(cls):
        ...

    def __repr__(self):
        ...

    @property
    def local_uuid(self):
        ...

    async def _deploy(self, *args, **kwargs) -> _ASYNC_H:
        ...

    def persist(self, label: str, namespace=1):
        ...

    @classmethod
    def from_name(cls: typing.Type[_ASYNC_P], app_name: str, tag: typing.Union[str, None] = None, namespace=1) -> _ASYNC_P:
        ...

    @classmethod
    async def lookup(cls, *args, **kwargs) -> _ASYNC_H:
        ...

    @classmethod
    async def _exists(cls, *args, **kwargs) -> bool:
        ...
