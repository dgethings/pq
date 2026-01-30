"""Test script to verify enhanced error messages."""

from pathlib import Path
from pq.loader import load_document
from pq.evaluator import evaluate_query, QueryEvaluationError


def test_error_messages():
    """Test that error messages are user-friendly."""
    print("Loading test data...")
    data = load_document(file_path=Path("test_data.json"))
    print()

    test_cases = [
        ("", "Empty expression"),
        ("data['nonexistent']", "Missing key"),
        ("invalid_var", "Invalid variable"),
        ("data['items'][0]['name'](5)", "Calling a non-function"),
        ("data['items'][999]", "Index out of range"),
        ("data['items'][0] + 'string'", "Type error"),
        ("data['items'[0]]", "Syntax error"),
    ]

    for query, description in test_cases:
        print(f"Test: {description}")
        print(f"Query: {query}")
        try:
            result = evaluate_query(query, data)
            print(f"Result: {result}")
        except QueryEvaluationError as e:
            print(f"Error: {e}")
        print()

    print("All error message tests passed!")


if __name__ == "__main__":
    test_error_messages()
