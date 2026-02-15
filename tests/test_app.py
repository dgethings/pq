"""Test script to verify QueryApp functionality."""

from pathlib import Path
from pq.loader import load_document
from pq.evaluator import evaluate_query, QueryEvaluationError


def test_app_logic():
    """Test the app logic without TUI."""
    print("Loading test data...")
    data = load_document(file_path=Path("tests/test_data.json"))
    print(f"Loaded data with keys: {list(data.keys())}")
    print()

    print("Test 1: Simple query")
    result = evaluate_query("_['items'][0]['name']", data)
    print("Query: _['items'][0]['name']")
    print(f"Result: {result}")
    print()

    print("Test 2: List comprehension")
    result = evaluate_query("[item['name'] for item in _['items']]", data)
    print("Query: [item['name'] for item in _['items']]")
    print(f"Result: {result}")
    print()

    print("Test 3: Filtered list")
    result = evaluate_query("[item for item in _['items'] if item['age'] > 25]", data)
    print("Query: [item for item in _['items'] if item['age'] > 25]")
    print(f"Result: {result}")
    print()

    print("Test 4: Error handling")
    try:
        result = evaluate_query("_['nonexistent_key']", data)
    except QueryEvaluationError as e:
        print("Query: _['nonexistent_key']")
        print(f"Error (expected): {e}")
    print()

    print("Test 5: Metadata access")
    result = evaluate_query("_['metadata']['version']", data)
    print("Query: _['metadata']['version']")
    print(f"Result: {result}")
    print()

    print("Test 6: Counter - count cities")
    result = evaluate_query("Counter(item['city'] for item in _['items'])", data)
    print("Query: Counter(item['city'] for item in _['items'])")
    print(f"Result: {result}")
    print()

    print("Test 7: Counter - count ages")
    result = evaluate_query("Counter([x['age'] for x in _['items']])", data)
    print("Query: Counter([x['age'] for x in _['items']])")
    print(f"Result: {result}")
    print()

    print("Test 8: namedtuple - create structured data")
    result = evaluate_query(
        "namedtuple('Person', 'name age')(_['items'][0]['name'], _['items'][0]['age'])",
        data,
    )
    print(
        "Query: namedtuple('Person', 'name age')(_['items'][0]['name'], _['items'][0]['age'])"
    )
    print(f"Result: {result}")
    print()

    print("Test 9: defaultdict - handle missing keys")
    result = evaluate_query("defaultdict(list, {'a': [1, 2]})", data)
    print("Query: defaultdict(list, {'a': [1, 2]})")
    print(f"Result: {result}")
    print()

    print("All tests passed!")


if __name__ == "__main__":
    test_app_logic()
