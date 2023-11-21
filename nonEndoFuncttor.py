from __future__ import annotations
from typing import Any, Callable

class ListFunctor:
    def __init__(self, values: list[Any]) -> None:
        self.values = values
    def map(self, func: Callable[[Any], Any]):
        return ListFunctor([func(value) for value in self.values])

## this class is not an endofunctor it is a normal functor
class StringFunctor: 
    def __init__(self, value: str) -> None:
        self.value = value
    def map(self, func: Callable[[str], str]):
        return ListFunctor([func(self.value)])


def main() -> None:
    sf = StringFunctor("Hello")
    lf = sf.map(len) ## this is not a StringFunctor so the shape has changed.
    print(lf.values)

    lf2 = lf.map(lambda x:  x * x )
    print(lf2.values)


if __name__ == "__main__":
    main()
