from typing import Any


class SingletonMeta(type):
    _instances: dict[type, object] = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwds)
            cls._instances[cls] = instance

        return cls._instances
