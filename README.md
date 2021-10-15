# Non-English documentaion
[Russian | Русский](/docs/Russian.md)
# SOON (PRE-ALPHA)

## What is petuhlang?
Petuhlang is a joke-like language, based on Python.
It updates builtins to make a new syntax based on operators rewrite.
## Classes
```monkey
from petuhlang import build
build.using >> "petuhlang"


class PythonClass:
    def foo(self) -> None:
        print("bar")


pyclass >> MyClass(extends=PythonClass)


function >> main(
    arg("user") >> str,
    kwarg("greeting", value="Hello") >> str,
) [
    MyClass.createInstance(bindTo="instance") >> then [
        console.log(f"It works:) -> {instance.__class__.__name__}")
    ]
]

main()
```

## Base functions
```monkey
from petuhlang import build
build.using >> "petuhlang"


function >> main() [
    retrieve >> (1 + 1)
]

console.log(main())
```
