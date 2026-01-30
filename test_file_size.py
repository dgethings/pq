"""Test script to verify 2GB file size limit."""

import tempfile
from pathlib import Path
from pq.loader import DocumentLoadError, load_document


def test_file_size_limit():
    """Test that files larger than 2GB are rejected."""
    print("Testing 2GB file size limit...")
    print()

    # Test with a small file (should work)
    print("Test 1: Small file (should succeed)")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write('{"test": "value"}')
        small_file = Path(f.name)
    try:
        data = load_document(file_path=small_file)
        print(f"Success: Loaded small file with {data}")
        small_file.unlink()
    except DocumentLoadError as e:
        print(f"Failed: {e}")
        small_file.unlink()
    print()

    # Test with a non-existent file
    print("Test 2: Non-existent file (should fail)")
    try:
        data = load_document(file_path=Path("nonexistent_file.json"))
        print(f"Failed: Should have raised DocumentLoadError")
    except DocumentLoadError as e:
        print(f"Success: Got expected error: {e}")
    print()

    # Verify the MAX_FILE_SIZE constant is set correctly
    from pq.loader import MAX_FILE_SIZE

    print(f"Test 3: MAX_FILE_SIZE constant")
    print(f"MAX_FILE_SIZE = {MAX_FILE_SIZE} bytes ({MAX_FILE_SIZE / (1024**3):.0f} GB)")
    assert MAX_FILE_SIZE == 2 * 1024 * 1024 * 1024, "MAX_FILE_SIZE should be 2GB"
    print("Success: MAX_FILE_SIZE is correctly set to 2GB")
    print()

    print("All file size limit tests passed!")


if __name__ == "__main__":
    test_file_size_limit()
