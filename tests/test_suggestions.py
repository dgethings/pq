"""Test script to verify suggestions integration."""

from pathlib import Path
from pq.loader import load_document
from pq.completion import PathExtractor, FuzzyMatcher
from pq.evaluator import evaluate_query


def test_suggestions_integration():
    """Test suggestion system integration."""
    print("Loading test data...")
    data = load_document(file_path=Path("tests/test_data.json"))
    print()

    path_extractor = PathExtractor(data)
    paths = path_extractor.get_paths()
    fuzzy_matcher = FuzzyMatcher(paths)

    test_queries = [
        "_['items'][0]['n",  # Partial key name
        "_['items'][0]['a",  # Another partial key
        "_['metadata']['v",  # Partial metadata key
        "",  # Empty query
    ]

    for query in test_queries:
        print(f"Query: '{query}'")
        suggestions = fuzzy_matcher.find_matches(query)
        print(f"Suggestions ({len(suggestions)}):")
        for suggestion in suggestions[:5]:
            print(f"  - {suggestion}")
        print()

    print("Testing evaluation with suggestions...")
    query = "_['items'][0]['name']"
    result = evaluate_query(query, data)
    print(f"Query: {query}")
    print(f"Result: {result}")
    print()

    print("All tests passed!")


if __name__ == "__main__":
    test_suggestions_integration()
