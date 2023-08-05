from time import time_ns
from multipledispatch import dispatch


class Temporisation:
    @dispatch()
    def __init__(self) -> None:
        # tempo en ms
        self._val_temporisation: int = 0
        self._state: int = 0
        self._my_time: int = time_ns()

    @dispatch(int)
    def __init__(self, duree_ms: int) -> None:
        # tempo en ms
        self._val_temporisation: int = duree_ms * 1000000
        self._state: int = 0
        self._my_time: int = self._val_temporisation

    def start(self, trigger: bool = True) -> None:
        if trigger:
            self._my_time: int = time_ns()
            self._state: int = 1

    def stop(self) -> None:
        self._state: int = 0

    def state(self):
        return self._state

    def is_on(self) -> bool:
        return time_ns() - self._my_time < self._val_temporisation

    def is_off(self) -> bool:
        return time_ns() - self._my_time >= self._val_temporisation

    def valid(self) -> bool:
        return self._val_temporisation != 0

    def set_tempo(self, duree_ms: int) -> None:
        self._val_temporisation: int = duree_ms * 1000000

    def get_tempo(self) -> int:
        return self._val_temporisation


class Temporisation_ms(Temporisation):
    def __init__(self, duree_ms: int) -> None:
        super().__init__(duree_ms)


class Temporisation_s(Temporisation):
    def __init__(self, duree_s: int) -> None:
        super().__init__(duree_s * 1000)
