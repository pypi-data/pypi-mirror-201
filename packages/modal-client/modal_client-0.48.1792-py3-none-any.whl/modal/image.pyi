import __main__
import modal._resolver
import modal.gpu
import modal.mount
import modal.object
import modal.secret
import modal.shared_volume
import modal_proto.api_pb2
import pathlib
import typing

def _validate_python_version(version: str) -> None:
    ...


def _dockerhub_python_version(python_version=None):
    ...


def _get_client_requirements_path():
    ...


def _flatten_str_args(function_name: str, arg_name: str, args: typing.Tuple[typing.Union[str, typing.List[str]], ...]) -> typing.List[str]:
    ...


class _ImageHandle(modal.object._Handle):
    def _is_inside(self) -> bool:
        ...


class _ImageRegistryConfig:
    def __init__(self, registry_type: int = 0, secret: typing.Union[modal.secret._Secret, None] = None):
        ...

    async def resolve(self, resolver: modal._resolver.Resolver) -> modal_proto.api_pb2.ImageRegistryConfig:
        ...


class _Image(modal.object._Provider[_ImageHandle]):
    @staticmethod
    def _from_args(base_images={}, context_files={}, dockerfile_commands: typing.Union[typing.List[str], typing.Callable[[], typing.List[str]]] = [], secrets: typing.Sequence[modal.secret._Secret] = [], ref=None, gpu_config: typing.Union[modal_proto.api_pb2.GPUConfig, None] = None, build_function=None, context_mount: typing.Union[modal.mount._Mount, None] = None, image_registry_config: typing.Union[_ImageRegistryConfig, None] = None):
        ...

    def extend(self, *, context_files={}, dockerfile_commands: typing.Union[typing.List[str], typing.Callable[[], typing.List[str]]] = [], secrets: typing.Sequence[modal.secret._Secret] = [], ref=None, gpu_config: typing.Union[modal_proto.api_pb2.GPUConfig, None] = None, build_function=None, context_mount: typing.Union[modal.mount._Mount, None] = None, image_registry_config: typing.Union[_ImageRegistryConfig, None] = None) -> _Image:
        ...

    def copy(self, mount: modal.mount._Mount, remote_path: typing.Union[str, pathlib.Path] = '.') -> _Image:
        ...

    def pip_install(self, *packages: typing.Union[str, typing.List[str]], find_links: typing.Union[str, None] = None, index_url: typing.Union[str, None] = None, extra_index_url: typing.Union[str, None] = None, pre: bool = False) -> _Image:
        ...

    def pip_install_private_repos(self, *repositories: str, git_user: str, secrets: typing.Sequence[modal.secret._Secret] = []) -> _Image:
        ...

    def pip_install_from_requirements(self, requirements_txt: str, find_links: typing.Union[str, None] = None) -> _Image:
        ...

    def pip_install_from_pyproject(self, pyproject_toml: str, optional_dependencies: typing.List[str] = []) -> _Image:
        ...

    def poetry_install_from_file(self, poetry_pyproject_toml: str, poetry_lockfile: typing.Union[str, None] = None, ignore_lockfile: bool = False, old_installer: bool = False) -> _Image:
        ...

    def dockerfile_commands(self, dockerfile_commands: typing.Union[str, typing.List[str]], context_files: typing.Dict[str, str] = {}, secrets: typing.Sequence[modal.secret._Secret] = [], gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, context_mount: typing.Union[modal.mount._Mount, None] = None) -> _Image:
        ...

    def run_commands(self, *commands: typing.Union[str, typing.List[str]], secrets: typing.Sequence[modal.secret._Secret] = [], gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None) -> _Image:
        ...

    @staticmethod
    def conda(python_version: str = '3.9') -> _Image:
        ...

    def conda_install(self, *packages: typing.Union[str, typing.List[str]], channels: typing.List[str] = []) -> _Image:
        ...

    def conda_update_from_environment(self, environment_yml: str) -> _Image:
        ...

    @staticmethod
    def micromamba(python_version: str = '3.9') -> _Image:
        ...

    @staticmethod
    def _registry_setup_commands(tag: str, setup_dockerfile_commands: typing.List[str], setup_commands: typing.List[str]) -> typing.List[str]:
        ...

    @staticmethod
    def from_dockerhub(tag: str, setup_dockerfile_commands: typing.List[str] = [], setup_commands: typing.List[str] = [], **kwargs) -> _Image:
        ...

    @staticmethod
    def from_gcp_artifact_registry(tag: str, secret: typing.Union[modal.secret._Secret, None] = None, setup_dockerfile_commands: typing.List[str] = [], **kwargs) -> _Image:
        ...

    @staticmethod
    def from_aws_ecr(tag: str, secret: typing.Union[modal.secret._Secret, None] = None, setup_dockerfile_commands: typing.List[str] = [], setup_commands: typing.List[str] = [], **kwargs) -> _Image:
        ...

    @staticmethod
    def from_dockerfile(path: typing.Union[str, pathlib.Path], context_mount: typing.Union[modal.mount._Mount, None] = None) -> _Image:
        ...

    @staticmethod
    def debian_slim(python_version: typing.Union[str, None] = None) -> _Image:
        ...

    def apt_install(self, *packages: typing.Union[str, typing.List[str]]) -> _Image:
        ...

    def run_function(self, raw_f: typing.Callable[[], typing.Any], *, secret: typing.Union[modal.secret._Secret, None] = None, secrets: typing.Sequence[modal.secret._Secret] = (), gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, mounts: typing.Sequence[modal.mount._Mount] = (), shared_volumes: typing.Dict[str, modal.shared_volume._SharedVolume] = {}, cpu: typing.Union[float, None] = None, memory: typing.Union[int, None] = None, timeout: typing.Union[int, None] = 86400, cloud: typing.Union[str, None] = None) -> _Image:
        ...

    def env(self, vars: typing.Dict[str, str]) -> _Image:
        ...


class ImageHandle(modal.object.Handle):
    def __init__(self):
        ...

    def _is_inside(self) -> bool:
        ...


class AioImageHandle(modal.object.AioHandle):
    def __init__(self):
        ...

    def _is_inside(self) -> bool:
        ...


class Image(modal.object.Provider[ImageHandle]):
    def __init__(self, load: typing.Callable[[modal._resolver.Resolver, str], modal.object._BLOCKING_H], rep: str):
        ...

    @staticmethod
    def _from_args(base_images={}, context_files={}, dockerfile_commands: typing.Union[typing.List[str], typing.Callable[[], typing.List[str]]] = [], secrets: typing.Sequence[modal.secret.Secret] = [], ref=None, gpu_config: typing.Union[modal_proto.api_pb2.GPUConfig, None] = None, build_function=None, context_mount: typing.Union[modal.mount.Mount, None] = None, image_registry_config: typing.Union[_ImageRegistryConfig, None] = None):
        ...

    def extend(self, **kwargs) -> Image:
        ...

    def copy(self, mount: modal.mount.Mount, remote_path: typing.Union[str, pathlib.Path] = '.') -> Image:
        ...

    def pip_install(self, *packages: typing.Union[str, typing.List[str]], find_links: typing.Union[str, None] = None, index_url: typing.Union[str, None] = None, extra_index_url: typing.Union[str, None] = None, pre: bool = False) -> Image:
        ...

    def pip_install_private_repos(self, *repositories: str, git_user: str, secrets: typing.Sequence[modal.secret.Secret] = []) -> Image:
        ...

    def pip_install_from_requirements(self, requirements_txt: str, find_links: typing.Union[str, None] = None) -> Image:
        ...

    def pip_install_from_pyproject(self, pyproject_toml: str, optional_dependencies: typing.List[str] = []) -> Image:
        ...

    def poetry_install_from_file(self, poetry_pyproject_toml: str, poetry_lockfile: typing.Union[str, None] = None, ignore_lockfile: bool = False, old_installer: bool = False) -> Image:
        ...

    def dockerfile_commands(self, dockerfile_commands: typing.Union[str, typing.List[str]], context_files: typing.Dict[str, str] = {}, secrets: typing.Sequence[modal.secret.Secret] = [], gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, context_mount: typing.Union[modal.mount.Mount, None] = None) -> Image:
        ...

    def run_commands(self, *commands: typing.Union[str, typing.List[str]], secrets: typing.Sequence[modal.secret.Secret] = [], gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None) -> Image:
        ...

    @staticmethod
    def conda(python_version: str = '3.9') -> Image:
        ...

    def conda_install(self, *packages: typing.Union[str, typing.List[str]], channels: typing.List[str] = []) -> Image:
        ...

    def conda_update_from_environment(self, environment_yml: str) -> Image:
        ...

    @staticmethod
    def micromamba(python_version: str = '3.9') -> Image:
        ...

    @staticmethod
    def _registry_setup_commands(tag: str, setup_dockerfile_commands: typing.List[str], setup_commands: typing.List[str]) -> typing.List[str]:
        ...

    @staticmethod
    def from_dockerhub(tag: str, setup_dockerfile_commands: typing.List[str] = [], setup_commands: typing.List[str] = [], **kwargs) -> Image:
        ...

    @staticmethod
    def from_gcp_artifact_registry(tag: str, secret: typing.Union[modal.secret.Secret, None] = None, setup_dockerfile_commands: typing.List[str] = [], **kwargs) -> Image:
        ...

    @staticmethod
    def from_aws_ecr(tag: str, secret: typing.Union[modal.secret.Secret, None] = None, setup_dockerfile_commands: typing.List[str] = [], setup_commands: typing.List[str] = [], **kwargs) -> Image:
        ...

    @staticmethod
    def from_dockerfile(path: typing.Union[str, pathlib.Path], context_mount: typing.Union[modal.mount.Mount, None] = None) -> Image:
        ...

    @staticmethod
    def debian_slim(python_version: typing.Union[str, None] = None) -> Image:
        ...

    def apt_install(self, *packages: typing.Union[str, typing.List[str]]) -> Image:
        ...

    def run_function(self, raw_f: typing.Callable[[], typing.Any], *, secret: typing.Union[modal.secret.Secret, None] = None, secrets: typing.Sequence[modal.secret.Secret] = (), gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, mounts: typing.Sequence[modal.mount.Mount] = (), shared_volumes: typing.Dict[str, modal.shared_volume.SharedVolume] = {}, cpu: typing.Union[float, None] = None, memory: typing.Union[int, None] = None, timeout: typing.Union[int, None] = 86400, cloud: typing.Union[str, None] = None) -> Image:
        ...

    def env(self, vars: typing.Dict[str, str]) -> Image:
        ...


class AioImage(modal.object.AioProvider[AioImageHandle]):
    def __init__(self, load: typing.Callable[[modal._resolver.Resolver, str], typing.Awaitable[modal.object._ASYNC_H]], rep: str):
        ...

    @staticmethod
    def _from_args(base_images={}, context_files={}, dockerfile_commands: typing.Union[typing.List[str], typing.Callable[[], typing.List[str]]] = [], secrets: typing.Sequence[modal.secret.AioSecret] = [], ref=None, gpu_config: typing.Union[modal_proto.api_pb2.GPUConfig, None] = None, build_function=None, context_mount: typing.Union[modal.mount.AioMount, None] = None, image_registry_config: typing.Union[_ImageRegistryConfig, None] = None):
        ...

    def extend(self, **kwargs) -> AioImage:
        ...

    def copy(self, mount: modal.mount.AioMount, remote_path: typing.Union[str, pathlib.Path] = '.') -> AioImage:
        ...

    def pip_install(self, *packages: typing.Union[str, typing.List[str]], find_links: typing.Union[str, None] = None, index_url: typing.Union[str, None] = None, extra_index_url: typing.Union[str, None] = None, pre: bool = False) -> AioImage:
        ...

    def pip_install_private_repos(self, *repositories: str, git_user: str, secrets: typing.Sequence[modal.secret.AioSecret] = []) -> AioImage:
        ...

    def pip_install_from_requirements(self, requirements_txt: str, find_links: typing.Union[str, None] = None) -> AioImage:
        ...

    def pip_install_from_pyproject(self, pyproject_toml: str, optional_dependencies: typing.List[str] = []) -> AioImage:
        ...

    def poetry_install_from_file(self, poetry_pyproject_toml: str, poetry_lockfile: typing.Union[str, None] = None, ignore_lockfile: bool = False, old_installer: bool = False) -> AioImage:
        ...

    def dockerfile_commands(self, dockerfile_commands: typing.Union[str, typing.List[str]], context_files: typing.Dict[str, str] = {}, secrets: typing.Sequence[modal.secret.AioSecret] = [], gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, context_mount: typing.Union[modal.mount.AioMount, None] = None) -> AioImage:
        ...

    def run_commands(self, *commands: typing.Union[str, typing.List[str]], secrets: typing.Sequence[modal.secret.AioSecret] = [], gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None) -> AioImage:
        ...

    @staticmethod
    def conda(python_version: str = '3.9') -> AioImage:
        ...

    def conda_install(self, *packages: typing.Union[str, typing.List[str]], channels: typing.List[str] = []) -> AioImage:
        ...

    def conda_update_from_environment(self, environment_yml: str) -> AioImage:
        ...

    @staticmethod
    def micromamba(python_version: str = '3.9') -> AioImage:
        ...

    @staticmethod
    def _registry_setup_commands(tag: str, setup_dockerfile_commands: typing.List[str], setup_commands: typing.List[str]) -> typing.List[str]:
        ...

    @staticmethod
    def from_dockerhub(tag: str, setup_dockerfile_commands: typing.List[str] = [], setup_commands: typing.List[str] = [], **kwargs) -> AioImage:
        ...

    @staticmethod
    def from_gcp_artifact_registry(tag: str, secret: typing.Union[modal.secret.AioSecret, None] = None, setup_dockerfile_commands: typing.List[str] = [], **kwargs) -> AioImage:
        ...

    @staticmethod
    def from_aws_ecr(tag: str, secret: typing.Union[modal.secret.AioSecret, None] = None, setup_dockerfile_commands: typing.List[str] = [], setup_commands: typing.List[str] = [], **kwargs) -> AioImage:
        ...

    @staticmethod
    def from_dockerfile(path: typing.Union[str, pathlib.Path], context_mount: typing.Union[modal.mount.AioMount, None] = None) -> AioImage:
        ...

    @staticmethod
    def debian_slim(python_version: typing.Union[str, None] = None) -> AioImage:
        ...

    def apt_install(self, *packages: typing.Union[str, typing.List[str]]) -> AioImage:
        ...

    def run_function(self, raw_f: typing.Callable[[], typing.Any], *, secret: typing.Union[modal.secret.AioSecret, None] = None, secrets: typing.Sequence[modal.secret.AioSecret] = (), gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, mounts: typing.Sequence[modal.mount.AioMount] = (), shared_volumes: typing.Dict[str, modal.shared_volume.AioSharedVolume] = {}, cpu: typing.Union[float, None] = None, memory: typing.Union[int, None] = None, timeout: typing.Union[int, None] = 86400, cloud: typing.Union[str, None] = None) -> AioImage:
        ...

    def env(self, vars: typing.Dict[str, str]) -> AioImage:
        ...
