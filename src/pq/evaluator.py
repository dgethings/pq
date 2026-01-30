"""Query evaluation module."""

from typing import Any


ALLOWED_BUILTINS = {
    "len": len,
    "sum": sum,
    "min": min,
    "max": max,
    "sorted": sorted,
    "filter": filter,
    "map": map,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "type": type,
    "isinstance": isinstance,
    "range": range,
    "zip": zip,
    "enumerate": enumerate,
    "any": any,
    "all": all,
    "abs": abs,
    "round": round,
    "slice": slice,
}


class QueryEvaluationError(Exception):
    """Raised when query evaluation fails."""


def evaluate_query(expression: str, data: dict[str, Any]) -> Any:
    """Safely evaluate a Python expression with data context.

    Args:
        expression: Python expression to evaluate
        data: Document data available as 'data' variable

    Returns:
        Result of the expression evaluation

    Raises:
        QueryEvaluationError: If expression is invalid or evaluation fails
    """
    if not expression.strip():
        raise QueryEvaluationError(
            "Please enter a query. Try: data, data['key'], or data['items'][0]"
        )

    restricted_globals = {
        "__builtins__": ALLOWED_BUILTINS,
        "data": data,
    }

    try:
        result = eval(expression, restricted_globals, {})
        return result
    except SyntaxError as e:
        raise QueryEvaluationError(
            f"Invalid Python syntax: {e.msg} at position {e.offset}. "
            f"Check for missing quotes, brackets, or operators."
        )
    except NameError as e:
        name = str(e).split("'")[1]
        available = ", ".join(sorted(ALLOWED_BUILTINS.keys())[:5])
        raise QueryEvaluationError(
            f"'{name}' is not available. "
            f"Use 'data' to access the document. Available functions: {available}, ..."
        )
    except TypeError as e:
        error_msg = str(e)
        if "subscriptable" in error_msg:
            raise QueryEvaluationError(
                f"Cannot use brackets on this type. "
                f"Make sure you're accessing a dictionary or list, not a string or number."
            )
        elif "not iterable" in error_msg:
            raise QueryEvaluationError(
                f"This value cannot be iterated over. "
                f"Use it directly or check if it's a list or dict first."
            )
        else:
            raise QueryEvaluationError(f"Type mismatch: {error_msg}")
    except KeyError as e:
        key = str(e).strip("'\"")
        raise QueryEvaluationError(
            f"Key '{key}' not found. "
            f"Check the document structure or use fuzzy matching to find available keys."
        )
    except AttributeError as e:
        raise QueryEvaluationError(
            f"Invalid attribute access: {e}. "
            f"Use dictionary-style access with brackets: data['key']"
        )
    except ValueError as e:
        raise QueryEvaluationError(f"Invalid value: {e}")
    except IndexError as e:
        raise QueryEvaluationError(
            f"Index out of range. "
            f"The list is shorter than the index you're trying to access."
        )
    except Exception as e:
        raise QueryEvaluationError(f"Query evaluation failed: {e}")
