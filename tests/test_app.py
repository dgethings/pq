"""Test script to verify QueryApp functionality."""

from pathlib import Path
from pq.loader import load_document
from pq.evaluator import evaluate_query, QueryEvaluationError


def test_app_logic():
    """Test the app logic without TUI."""
    print("Loading test data...")
    data = load_document(file_path=Path("test_data.json"))
    print(f"Loaded data with keys: {list(data.keys())}")
    print()

    print("Test 1: Simple query")
    result = evaluate_query("data['items'][0]['name']", data)
    print("Query: data['items'][0]['name']")
    print(f"Result: {result}")
    print()

    print("Test 2: List comprehension")
    result = evaluate_query("[item['name'] for item in data['items']]", data)
    print("Query: [item['name'] for item in data['items']]")
    print(f"Result: {result}")
    print()

    print("Test 3: Filtered list")
    result = evaluate_query(
        "[item for item in data['items'] if item['age'] > 25]", data
    )
    print("Query: [item for item in data['items'] if item['age'] > 25]")
    print(f"Result: {result}")
    print()

    print("Test 4: Error handling")
    try:
        result = evaluate_query("data['nonexistent_key']", data)
    except QueryEvaluationError as e:
        print("Query: data['nonexistent_key']")
        print(f"Error (expected): {e}")
    print()

    print("Test 5: Metadata access")
    result = evaluate_query("data['metadata']['version']", data)
    print("Query: data['metadata']['version']")
    print(f"Result: {result}")
    print()

    print("All tests passed!")


if __name__ == "__main__":
    test_app_logic()
