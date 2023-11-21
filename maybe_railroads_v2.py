from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar, Optional

T = TypeVar("T")
U = TypeVar("U")

class Maybe(Generic[T]):

    def __init__(self, value: Optional[T]) -> None:
        self.value = value
    
    def bind(self, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        return self if self.value == None else func(self.value)

    __match_args__ = ("value",)

    def __match__(self, other: Maybe[T]) -> bool:
        return self.value == other.value
    
    @staticmethod
    def unit(value: Any) -> Maybe[Any]:
        return Maybe(value)

def maybe(func: Callable[...,Any]) -> Callable[...,Any]:
    def wrapper(*args: Any, **kwargs: Any):
        try:
            return Maybe(func(*args, **kwargs))
        except Exception:
            return Maybe(None)

    return wrapper


@maybe
def parse_int(value: str) -> int:
    return int(value)
    

@maybe
def double(value: int) -> int:
    return 2 * value    

def is_positive(value) -> Maybe[int]:
    return Maybe(value) if value > 0 else Maybe(None)

def validate_and_process(input_str: str) -> Maybe[str] | Maybe[int]:
    return (
        Maybe(input_str)
        .bind(parse_int)
        .bind(is_positive)
        .bind(double)
    )

def main() -> None:
    inputs = [ "5", "-3", "foo"]  

    for input_str in inputs:
        print(f"Processing '{input_str}':")
        result = validate_and_process(input_str)
        print(result.value)
        match result:
            case Maybe(None):
                print(f"Invalid input: '{input_str}'")
            case Maybe(value=int()):
                print(f"Result: {result.value} ")
            case _:
                print("Unexpected input")
    print("DONE!")

if __name__ == "__main__":
    main()
