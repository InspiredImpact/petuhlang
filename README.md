# SOON (PRE-ALPHA)

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