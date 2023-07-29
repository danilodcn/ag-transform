import abc


class EntityDoesNotExist(Exception):
    ...


class Repository(abc.ABC):
    @abc.abstractproperty
    def DoesNotExist(self) -> EntityDoesNotExist:
        raise NotImplementedError
