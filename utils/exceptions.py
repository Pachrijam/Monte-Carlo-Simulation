def safe_int(prompt: str, min_val: int = None, max_val: int = None) -> int:
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                raise ValueError(f"Value must be at least {min_val}")
            if max_val is not None and value > max_val:
                raise ValueError(f"Value must be at most {max_val}")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}")


def safe_float(prompt: str, min_val: float = None, max_val: float = None) -> float:
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                raise ValueError(f"Value must be at least {min_val}")
            if max_val is not None and value > max_val:
                raise ValueError(f"Value must be at most {max_val}")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}")


def safe_choice(prompt: str, valid_options: list) -> str:
    while True:
        try:
            value = input(prompt).strip().lower()
            if value not in valid_options:
                raise ValueError(f"Please enter one of: {', '.join(valid_options)}")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}")


def safe_optional_int(prompt: str, default: int = None) -> int:
    while True:
        try:
            value_str = input(prompt).strip()
            if not value_str:
                if default is not None:
                    return default
                raise ValueError("Input required")
            value = int(value_str)
            return value
        except ValueError as e:
            print(f"Invalid input: {e}")


def safe_optional_float(prompt: str, default: float = None) -> float:
    while True:
        try:
            value_str = input(prompt).strip()
            if not value_str:
                if default is not None:
                    return default
                raise ValueError("Input required")
            value = float(value_str)
            return value
        except ValueError as e:
            print(f"Invalid input: {e}")


def safe_seed_input(prompt: str) -> int:
    while True:
        try:
            value_str = input(prompt).strip()
            if not value_str:
                return None
            if not value_str.isdigit():
                raise ValueError("Seed must be a non-negative integer")
            return int(value_str)
        except ValueError as e:
            print(f"Invalid input: {e}")
