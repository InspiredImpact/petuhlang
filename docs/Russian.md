# Не английская документация
[Russian | Русский](/docs/Russian.md)
# СКОРО (ПРЕ-АЛЬФА)

## Да кто такой этот ваш петухланг?
Петухланг это шуточный язык, основанный на Питоне.
Он перезагружает builtins чтобы воссоздать синтаксис основанный на перегрузке операторов.
## Классы
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
        console.log(f"Оно живое! -> {instance.__class__.__name__}")
    ]
]

main()
```

## Основные функции
```monkey
from petuhlang import build
build.using >> "petuhlang"


function >> main() [
    retrieve >> (1 + 1)
]

console.log(main())
```
