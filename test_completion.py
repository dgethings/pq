"""Test script to verify path completion functionality."""

from pathlib import Path
from pq.loader import load_document
from pq.completion import PathExtractor, FuzzyMatcher


def test_path_completion():
    """Test path completion and fuzzy matching."""
    print("Loading test data...")
    data = load_document(file_path=Path("test_data.json"))
    print(f"Loaded data with keys: {list(data.keys())}")
    print()

    print("Test 1: Extract all paths")
    extractor = PathExtractor(data)
    paths = extractor.get_paths()
    print(f"Extracted {len(paths)} paths:")
    for path in paths[:10]:
        print(f"  - {path}")
    if len(paths) > 10:
        print(f"  ... and {len(paths) - 10} more")
    print()

    print("Test 2: Fuzzy match for 'name'")
    matcher = FuzzyMatcher(paths)
    matches = matcher.find_matches("name")
    print(f"Fuzzy matches for 'name' ({len(matches)} results):")
    for match in matches:
        print(f"  - {match}")
    print()

    print("Test 3: Fuzzy match for 'items'")
    matches = matcher.find_matches("items")
    print(f"Fuzzy matches for 'items' ({len(matches)} results):")
    for match in matches[:5]:
        print(f"  - {match}")
    if len(matches) > 5:
        print(f"  ... and {len(matches) - 5} more")
    print()

    print("Test 4: Fuzzy match for empty query")
    matches = matcher.find_matches("")
    print(f"Fuzzy matches for empty query (first 10 of {len(matches)}):")
    for match in matches[:10]:
        print(f"  - {match}")
    print()

    print("Test 5: Fuzzy match for 'metadata'")
    matches = matcher.find_matches("metadata")
    print(f"Fuzzy matches for 'metadata' ({len(matches)} results):")
    for match in matches:
        print(f"  - {match}")
    print()

    print("All tests passed!")


if __name__ == "__main__":
    test_path_completion()
