class RegisterError(Exception):
    ...


class DependencyAlreadyExist(RegisterError):
    ...


class DependencyNotFound(RegisterError):
    ...
