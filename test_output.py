"""Test script to verify output formatting with different result types."""

from pq.output import OutputFormatter
from pq.evaluator import evaluate_query, QueryEvaluationError
from pathlib import Path
from pq.loader import load_document


def test_output_formatting():
    """Test output formatting for different result types."""
    print("Loading test data...")
    data = load_document(file_path=Path("test_data.json"))
    print()

    test_cases = [
        ("dict", data),
        ("list", data["items"]),
        ("string", data["items"][0]["name"]),
        ("integer", data["items"][0]["age"]),
        ("float", 3.14),
        ("boolean", data["items"][0]["active"]),
        ("None", None),
        ("list comprehension", [item["name"] for item in data["items"]]),
        ("filtered list", [item for item in data["items"] if item["age"] > 25]),
    ]

    for test_name, result in test_cases:
        print(f"Test: {test_name}")
        print(f"Type: {type(result).__name__}")
        print(f"Formatted output:")
        formatted = OutputFormatter.format_output(result)
        print(formatted)
        print()

    print("All output formatting tests passed!")


if __name__ == "__main__":
    test_output_formatting()
