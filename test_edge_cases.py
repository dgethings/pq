"""Test script to verify edge case handling."""

import tempfile
from pathlib import Path
from pq.loader import DocumentLoadError, load_document
from pq.evaluator import evaluate_query, QueryEvaluationError


def test_edge_cases():
    """Test edge cases like empty files, malformed JSON, etc."""
    print("Testing edge cases...")
    print()

    # Test with empty JSON object
    print("Test 1: Empty JSON object")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("{}")
        empty_file = Path(f.name)
    try:
        data = load_document(file_path=empty_file)
        print(f"Success: Loaded empty JSON object: {data}")
        empty_file.unlink()
    except DocumentLoadError as e:
        print(f"Failed: {e}")
        empty_file.unlink()
    print()

    # Test with JSON array (should fail - must be dict)
    print("Test 2: JSON array (should fail - must be dict)")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("[1, 2, 3]")
        array_file = Path(f.name)
    try:
        data = load_document(file_path=array_file)
        print(f"Failed: Should have raised DocumentLoadError, got: {data}")
        array_file.unlink()
    except DocumentLoadError as e:
        print(f"Success: Got expected error: {e}")
        array_file.unlink()
    print()

    # Test with malformed JSON
    print("Test 3: Malformed JSON")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write('{"invalid": json}')
        malformed_file = Path(f.name)
    try:
        data = load_document(file_path=malformed_file)
        print(f"Failed: Should have raised DocumentLoadError, got: {data}")
        malformed_file.unlink()
    except DocumentLoadError as e:
        print(f"Success: Got expected error: {e}")
        malformed_file.unlink()
    print()

    # Test with nested structures
    print("Test 4: Deeply nested structure")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write('{"a": {"b": {"c": {"d": {"e": "value"}}}}}')
        nested_file = Path(f.name)
    try:
        data = load_document(file_path=nested_file)
        result = evaluate_query("data['a']['b']['c']['d']['e']", data)
        print(f"Success: Deeply nested access: {result}")
        nested_file.unlink()
    except Exception as e:
        print(f"Failed: {e}")
        nested_file.unlink()
    print()

    # Test with special characters in JSON
    print("Test 5: Special characters in JSON")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write('{"key": "value with \\"quotes\\" and \\n newlines"}')
        special_file = Path(f.name)
    try:
        data = load_document(file_path=special_file)
        result = evaluate_query("data['key']", data)
        print(f"Success: Special characters: {result}")
        special_file.unlink()
    except Exception as e:
        print(f"Failed: {e}")
        special_file.unlink()
    print()

    # Test with very long list (performance test)
    print("Test 6: Large list (performance)")
    import json

    large_data = {"items": [{"id": i, "value": "test"} for i in range(1000)]}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write(json.dumps(large_data))
        large_file = Path(f.name)
    try:
        data = load_document(file_path=large_file)
        result = evaluate_query("len(data['items'])", data)
        print(f"Success: Large list length: {result}")
        large_file.unlink()
    except Exception as e:
        print(f"Failed: {e}")
        large_file.unlink()
    print()

    print("All edge case tests passed!")


if __name__ == "__main__":
    test_edge_cases()
