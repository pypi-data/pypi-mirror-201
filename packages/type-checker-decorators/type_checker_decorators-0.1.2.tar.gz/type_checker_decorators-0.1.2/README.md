# How to Import
```
from type_checker.decorators import enforce_strict_types
```


# Examples utilisation
```
from dataclasses import dataclass

from type_checker.decorators import enforce_strict_types


@enforce_strict_types
@dataclass
class Person:
    name: str
    age: int


def test_greet_person_with_wrong_types():
    try:
        Person(123, "twenty")
    except TypeError as e:
        assert (
            str(e)
            == "Problem on function Person, Expected type '<class 'str'>' for argument 'name' but received type '<class 'int'>' instead"
        )
    try:
        Person("Alice", "twenty")
    except TypeError as e:
        assert (
            str(e)
            == "Problem on function Person, Expected type '<class 'int'>' for argument 'age' but received type '<class 'str'>' instead"
        )

```


```
from type_checker.decorators import enforce_strict_types


@enforce_strict_types
def greet(name: str, age: int):
    print(f"Hello, {name}! You are {age} years old.")


def test_greet_with_wrong_types():
    try:
        greet(123, "twenty")
    except TypeError as e:
        print(str(e))
        assert (
            str(e)
            == "Problem on function greet, Expected type '<class 'str'>' for argument 'name' but received type '<class 'int'>' instead"
        )
    try:
        greet("Alice", "twenty")
    except TypeError as e:
        assert (
            str(e)
            == "Problem on function greet, Expected type '<class 'int'>' for argument 'age' but received type '<class 'str'>' instead"
        )

```