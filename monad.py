from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")

class Monad(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value
    
    def bind(self,func: Callable[[T], Monad[U]]) -> Monad[U]:
        return func(self.value)
    
    @staticmethod
    def unit(value: Any) -> Monad[Any]:
        return Monad(value)


def add_one(x: int) -> int:
    return x + 1

def multiply_by_two(x: int) -> int:
    return x * 2


def main() -> None:

    monad = Monad(5)    
    print(monad.value)    
    b = monad.bind(lambda x: Monad(add_one(x)))
    print(b.value)
    assert isinstance(b, Monad)
    assert(b.value == Monad(add_one(5)).value)

    # right identity
    # m.bind(unit) = m
    assert (monad.bind(Monad.unit).value == monad.value)

    # Associativity
    # m.bind(f).bind(g) = m.bind(lambda x: f(x).bind(g))
    assert(
        monad.bind(lambda x: Monad(add_one(x))).bind(lambda x: Monad(multiply_by_two(x))).value 
        == monad.bind(
            lambda x: Monad(add_one(x)).bind(lambda x: Monad(multiply_by_two(x)))
        ).value
    )
    

if __name__ == "__main__":
    main()
