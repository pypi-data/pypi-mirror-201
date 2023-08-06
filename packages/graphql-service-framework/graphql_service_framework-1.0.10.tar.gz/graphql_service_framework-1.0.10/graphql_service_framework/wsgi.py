from typing import Callable, Iterable

WSGIApp = Callable[[dict, Callable], Iterable[bytes]]
