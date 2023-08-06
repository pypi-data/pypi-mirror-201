import __main__
import modal._blob_utils
import modal._resolver
import modal.object
import pathlib
import typing

def client_mount_name():
    ...


class _MountEntry:
    remote_path: pathlib.PurePosixPath

    def description(self) -> str:
        ...

    def get_files_to_upload(self) -> typing.Iterator[typing.Tuple[pathlib.Path, str]]:
        ...

    def watch_entry(self) -> typing.Tuple[pathlib.Path, pathlib.Path]:
        ...


class _MountFile(_MountEntry):
    local_file: pathlib.Path
    remote_path: pathlib.PurePosixPath

    def description(self) -> str:
        ...

    def get_files_to_upload(self):
        ...

    def watch_entry(self):
        ...

    def __init__(self, local_file: pathlib.Path, remote_path: pathlib.PurePosixPath) -> None:
        ...

    def __repr__(self):
        ...

    def __eq__(self, other):
        ...


class _MountDir(_MountEntry):
    local_dir: pathlib.Path
    remote_path: pathlib.PurePosixPath
    condition: typing.Callable[[str], bool]
    recursive: bool

    def description(self):
        ...

    def get_files_to_upload(self):
        ...

    def watch_entry(self):
        ...

    def __init__(self, local_dir: pathlib.Path, remote_path: pathlib.PurePosixPath, condition: typing.Callable[[str], bool], recursive: bool) -> None:
        ...

    def __repr__(self):
        ...

    def __eq__(self, other):
        ...


class _MountHandle(modal.object._Handle):
    ...

class MountHandle(modal.object.Handle):
    def __init__(self):
        ...


class AioMountHandle(modal.object.AioHandle):
    def __init__(self):
        ...


class _Mount(modal.object._Provider[_MountHandle]):
    _entries: typing.List[_MountEntry]

    def __init__(self, remote_dir: typing.Union[str, pathlib.PurePosixPath] = None, *, local_dir: typing.Union[str, pathlib.Path, None] = None, local_file: typing.Union[str, pathlib.Path, None] = None, condition: typing.Union[typing.Callable[[str], bool], None] = None, recursive: bool = True, _entries: typing.Union[typing.List[_MountEntry], None] = None):
        ...

    def extend(self, *entries) -> _Mount:
        ...

    def is_local(self) -> bool:
        ...

    def add_local_dir(self, local_path: typing.Union[str, pathlib.Path], *, remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None, condition: typing.Union[typing.Callable[[str], bool], None] = None, recursive: bool = True) -> _Mount:
        ...

    @staticmethod
    def from_local_dir(local_path: typing.Union[str, pathlib.Path], *, remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None, condition: typing.Union[typing.Callable[[str], bool], None] = None, recursive: bool = True):
        ...

    def add_local_file(self, local_path: typing.Union[str, pathlib.Path], remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None) -> _Mount:
        ...

    @staticmethod
    def from_local_file(local_path: typing.Union[str, pathlib.Path], remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None) -> _Mount:
        ...

    def _description(self) -> str:
        ...

    def _get_files(self) -> typing.AsyncGenerator[modal._blob_utils.FileUploadSpec, None]:
        ...

    async def _load(self, resolver: modal._resolver.Resolver, existing_object_id: str):
        ...


class Mount(modal.object.Provider[MountHandle]):
    _entries: typing.List[_MountEntry]

    def __init__(self, remote_dir: typing.Union[str, pathlib.PurePosixPath] = None, *, local_dir: typing.Union[str, pathlib.Path, None] = None, local_file: typing.Union[str, pathlib.Path, None] = None, condition: typing.Union[typing.Callable[[str], bool], None] = None, recursive: bool = True, _entries: typing.Union[typing.List[_MountEntry], None] = None):
        ...

    def extend(self, *entries) -> Mount:
        ...

    def is_local(self) -> bool:
        ...

    def add_local_dir(self, local_path: typing.Union[str, pathlib.Path], *, remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None, condition: typing.Union[typing.Callable[[str], bool], None] = None, recursive: bool = True) -> Mount:
        ...

    @staticmethod
    def from_local_dir(local_path: typing.Union[str, pathlib.Path], *, remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None, condition: typing.Union[typing.Callable[[str], bool], None] = None, recursive: bool = True):
        ...

    def add_local_file(self, local_path: typing.Union[str, pathlib.Path], remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None) -> Mount:
        ...

    @staticmethod
    def from_local_file(local_path: typing.Union[str, pathlib.Path], remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None) -> Mount:
        ...

    def _description(self) -> str:
        ...

    def _get_files(self) -> typing.Generator[modal._blob_utils.FileUploadSpec, None, None]:
        ...

    def _load(self, resolver: modal._resolver.Resolver, existing_object_id: str):
        ...


class AioMount(modal.object.AioProvider[AioMountHandle]):
    _entries: typing.List[_MountEntry]

    def __init__(self, remote_dir: typing.Union[str, pathlib.PurePosixPath] = None, *, local_dir: typing.Union[str, pathlib.Path, None] = None, local_file: typing.Union[str, pathlib.Path, None] = None, condition: typing.Union[typing.Callable[[str], bool], None] = None, recursive: bool = True, _entries: typing.Union[typing.List[_MountEntry], None] = None):
        ...

    def extend(self, *entries) -> AioMount:
        ...

    def is_local(self) -> bool:
        ...

    def add_local_dir(self, local_path: typing.Union[str, pathlib.Path], *, remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None, condition: typing.Union[typing.Callable[[str], bool], None] = None, recursive: bool = True) -> AioMount:
        ...

    @staticmethod
    def from_local_dir(local_path: typing.Union[str, pathlib.Path], *, remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None, condition: typing.Union[typing.Callable[[str], bool], None] = None, recursive: bool = True):
        ...

    def add_local_file(self, local_path: typing.Union[str, pathlib.Path], remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None) -> AioMount:
        ...

    @staticmethod
    def from_local_file(local_path: typing.Union[str, pathlib.Path], remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None) -> AioMount:
        ...

    def _description(self) -> str:
        ...

    def _get_files(self) -> typing.AsyncGenerator[modal._blob_utils.FileUploadSpec, None]:
        ...

    async def _load(self, *args, **kwargs):
        ...


def _create_client_mount():
    ...


def _():
    ...


def aio_create_client_mount():
    ...


def _get_client_mount():
    ...


def _create_package_mounts(module_names: typing.Sequence[str]) -> typing.List[_Mount]:
    ...


def create_package_mounts(module_names: typing.Sequence[str]) -> typing.List[Mount]:
    ...


def aio_create_package_mounts(module_names: typing.Sequence[str]) -> typing.List[AioMount]:
    ...
