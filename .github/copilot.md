# Copilot Instructions for This Workspace

Follow these rules for all code generated or modified in this repository.

## <code_style>

* Do not include comments of any kind.
* Do not use docstrings or explanatory strings.
* Code must be self-explanatory through structure and naming alone.

## </code_style>

## <performance_>

* Prioritize performance over readability when there is a tradeoff.
* Prefer NumPy vectorized operations over Python loops.
* Avoid unnecessary allocations, copies, or intermediate structures.
* Eliminate redundant computation.
* Use efficient random sampling methods suited for Monte Carlo simulations.
* Only use parallelism when it provides clear performance gains.

## </performance_>

## <clarity_>

* Use clear, descriptive names for variables and functions.
* Avoid abbreviations unless they are standard (e.g., np, arr).
* Keep logic direct and minimal.

## </clarity_>

## <simplicity>

* Avoid unnecessary abstraction, classes, or indirection.
* Prefer straightforward functional implementations.
* Do not over-engineer solutions.

## </simplicity_>

## <consistency_>

* Maintain consistent naming patterns across the project.
* Keep formatting uniform.
* Reuse patterns that already exist in the codebase.

## </consistency_>

## <scope_control>

* Only read, modify, or reference files that are explicitly mentioned.
* Do not infer or assume the contents of unmentioned files.
* Do not introduce changes outside the requested scope.

## </scope_control>

## <verification_>

* After generating or modifying code, verify correctness using the terminal.
* Run relevant scripts, modules, or entry points to ensure execution succeeds.
* Check for runtime errors, incorrect outputs, and performance regressions.
* Prefer quick, direct execution commands over complex testing setups.
* Do not assume correctness without execution.

## </verification_>

## <one_shot_example>

Bad:

```id="w1r2kt"
def process(data):
    result = []
    for i in data:
        result.append(i * i)
    return result
```

Good:

```id="q7jv3c"
def square_values(values):
    return values * values
```

Bad:

```id="6b3nfd"
total = 0
for i in range(n):
    total += x
```

Good:

```id="n5p8xs"
total = x * n
```

Bad:

```id="t2m4ha"
samples = []
for _ in range(n):
    samples.append(random.random())
```

Good:

```id="k8z1dv"
samples = np.random.random(n)
```

## </one_shot_example>

## <summary_>

* No comments ever
* Performance-first
* Prefer vectorization
* Avoid unnecessary complexity
* Respect file scope strictly
* Verify using terminal execution
* Keep code concise and consistent

## </summary_>
