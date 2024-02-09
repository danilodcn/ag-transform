import abc


class EntityError(Exception):
    ...


class Repository(abc.ABC):
    @abc.abstractproperty
    def DoesNotExist(self) -> EntityError:
        raise NotImplementedError
