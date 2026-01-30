"""Test script to verify query evaluation performance."""

import time
from pathlib import Path
from pq.loader import load_document
from pq.evaluator import evaluate_query, QueryEvaluationError


def test_performance():
    """Test that query evaluation is fast enough."""
    print("Loading test data...")
    data = load_document(file_path=Path("test_data.json"))
    print()

    test_queries = [
        "data",
        "data['items']",
        "data['items'][0]",
        "data['items'][0]['name']",
        "data['metadata']",
        "data['metadata']['version']",
        "[item['name'] for item in data['items']]",
        "[item for item in data['items'] if item['age'] > 25]",
        "len(data['items'])",
        "data['items'][0]['name'] + ' test'",
    ]

    print("Testing query evaluation performance...")
    print()

    total_time = 0
    for query in test_queries:
        start_time = time.perf_counter()
        result = evaluate_query(query, data)
        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000
        total_time += elapsed_ms

        status = "✓" if elapsed_ms < 100 else "✗"
        print(f"{status} {query:60s} {elapsed_ms:6.2f}ms")

    avg_time = total_time / len(test_queries)
    print()
    print(f"Average time: {avg_time:.2f}ms")
    print(f"Total time: {total_time:.2f}ms")

    if avg_time < 100:
        print()
        print("✓ Performance test passed! Average evaluation time < 100ms")
    else:
        print()
        print("✗ Performance test failed! Average evaluation time >= 100ms")


if __name__ == "__main__":
    test_performance()
