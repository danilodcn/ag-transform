class RegistryError(Exception):
    ...


class DependencyAlreadyExist(RegistryError):
    ...


class DependencyNotFound(RegistryError):
    ...
