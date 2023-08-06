from .io_point import IoPoint

class IoTagDataDict(dict):
    def __setitem__(self, key: str, value: IoPoint) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be of type 'str'")
        if not isinstance(value, IoPoint):
            raise TypeError("Value must be of type 'IoPoint'")
        return super().__setitem__(key, value)

    def __getitem__(self, key: str) -> IoPoint:
        if not isinstance(key, str):
            raise TypeError("Key must be of type 'str'")
        return super().__getitem__(key)
