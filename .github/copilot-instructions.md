# Copilot instructions for this workspace

Follow these rules for all code generated or modified in this repository.

## <code_style>

* Do not include comments of any kind.
* This includes single-line comments, block comments, and docstrings.
* Do not use triple-quoted strings as explanations.
  </code_style>

## <clarity>

* Use clear, descriptive variable and function names.
* Write code that is self-explanatory without relying on comments.
* Prefer simple and direct logic over complex abstractions.

  </clarity>

## <readability>

* Keep code concise and clean.
* Avoid unnecessary verbosity or redundant structures.
* Ensure the purpose of the code is immediately understandable.

  </readability>

## <consistency>

* Maintain consistent naming conventions across files.
* Use predictable function and variable patterns.
* Keep formatting uniform throughout the project.

  </consistency>

## <one_shot_example>

Bad:

```
def f(x):
    return x * 3
```

Good:

```
def multiply_by_three(value):
    return value * 3
```

Bad:

```
def calc(a, b):
    return a / b
```

Good:

```
def divide(numerator, denominator):
    return numerator / denominator
```

Bad:

```
def process(d):
    r = []
    for i in d:
        r.append(i * 2)
    return r
```

Good:

```
def double_values(values):
    return [value * 2 for value in values]
```

</one_shot_example>

## summary

* No comments ever
* Prioritize naming clarity
* Prefer simple, readable logic
* Keep code concise and consistent

</summary>
