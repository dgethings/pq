"""Test collections module support in query evaluation."""

import pytest
from pathlib import Path
from collections import Counter, defaultdict, OrderedDict
from pq.loader import load_document
from pq.evaluator import evaluate_query


@pytest.fixture
def test_data():
    """Load test data for collections tests."""
    return load_document(file_path=Path("tests/test_data.json"))


class TestCounter:
    """Test Counter functionality."""

    def test_counter_with_list_comprehension(self, test_data):
        """Test Counter with a list comprehension."""
        result = evaluate_query(
            "Counter(item['city'] for item in _['items'])", test_data
        )
        assert isinstance(result, Counter)
        assert result["NYC"] == 2
        assert result["LA"] == 1

    def test_counter_with_list(self, test_data):
        """Test Counter with a list literal."""
        result = evaluate_query("Counter([x['age'] for x in _['items']])", test_data)
        assert isinstance(result, Counter)
        assert result[30] == 1
        assert result[25] == 1
        assert result[35] == 1

    def test_counter_with_dict_keys(self, test_data):
        """Test Counter with dictionary keys."""
        result = evaluate_query("Counter(_['metadata'].keys())", test_data)
        assert isinstance(result, Counter)
        assert len(result) == 3

    def test_counter_most_common(self, test_data):
        """Test Counter most_common method."""
        result = evaluate_query(
            "Counter(item['city'] for item in _['items']).most_common(1)", test_data
        )
        assert isinstance(result, list)
        assert result[0][0] == "NYC"
        assert result[0][1] == 2


class TestDefaultdict:
    """Test defaultdict functionality."""

    def test_defaultdict_basic(self, test_data):
        """Test basic defaultdict usage."""
        result = evaluate_query("defaultdict(list, {'a': [1], 'b': [2]})", test_data)
        assert isinstance(result, defaultdict)
        assert result["a"] == [1]
        assert result["b"] == [2]

    def test_defaultdict_missing_key(self, test_data):
        """Test defaultdict returns default for missing keys."""
        result = evaluate_query(
            "defaultdict(list, {}).get('nonexistent', [])", test_data
        )
        assert result == []

    def test_defaultdict_with_int_factory(self, test_data):
        """Test defaultdict with int factory."""
        result = evaluate_query("defaultdict(int, {'a': 1, 'b': 2})", test_data)
        assert isinstance(result, defaultdict)
        assert result["a"] == 1

    def test_defaultdict_conversion_to_dict(self, test_data):
        """Test converting defaultdict to regular dict."""
        result = evaluate_query("dict(defaultdict(list, {'a': [1]}))", test_data)
        assert isinstance(result, dict)
        assert result == {"a": [1]}


class TestOrderedDict:
    """Test OrderedDict functionality."""

    def test_ordereddict_basic(self, test_data):
        """Test basic OrderedDict usage."""
        result = evaluate_query(
            "list(OrderedDict([('a', 1), ('b', 2), ('c', 3)]).keys())", test_data
        )
        assert isinstance(result, list)
        assert result == ["a", "b", "c"]

    def test_ordereddict_preserves_order(self, test_data):
        """Test OrderedDict preserves insertion order."""
        result = evaluate_query(
            "list(OrderedDict([('x', 10), ('y', 20), ('z', 30)]).values())", test_data
        )
        assert result == [10, 20, 30]

    def test_ordereddict_from_dict(self, test_data):
        """Test OrderedDict from dict."""
        result = evaluate_query("OrderedDict(_['metadata'])", test_data)
        assert isinstance(result, OrderedDict)
        assert "count" in result
        assert "version" in result

    def test_ordereddict_items(self, test_data):
        """Test OrderedDict items."""
        result = evaluate_query(
            "list(OrderedDict([('a', 1), ('b', 2)]).items())", test_data
        )
        assert result == [("a", 1), ("b", 2)]


class TestDeque:
    """Test deque functionality."""

    def test_deque_basic(self, test_data):
        """Test basic deque usage."""
        result = evaluate_query("list(deque([1, 2, 3]))", test_data)
        assert result == [1, 2, 3]

    def test_deque_with_maxlen(self, test_data):
        """Test deque with maxlen."""
        result = evaluate_query("list(deque([1, 2, 3, 4, 5], maxlen=3))", test_data)
        assert result == [3, 4, 5]

    def test_deque_from_list_comprehension(self, test_data):
        """Test deque from list comprehension."""
        result = evaluate_query(
            "list(deque([item['age'] for item in _['items']]))", test_data
        )
        assert result == [30, 25, 35]

    def test_deque_operations(self, test_data):
        """Test deque with various operations."""
        result = evaluate_query("list(deque([1, 2, 3]) + deque([4, 5]))", test_data)
        assert result == [1, 2, 3, 4, 5]


class TestNamedtuple:
    """Test namedtuple functionality."""

    def test_namedtuple_creation(self, test_data):
        """Test creating and using namedtuple."""
        result = evaluate_query("namedtuple('Point', 'x y')(1, 2)", test_data)
        assert result.x == 1
        assert result.y == 2
        assert result[0] == 1
        assert result[1] == 2

    def test_namedtuple_list(self, test_data):
        """Test namedtuple converted to list."""
        result = evaluate_query(
            "list(namedtuple('Point', 'x y z')(1, 2, 3))", test_data
        )
        assert result == [1, 2, 3]

    def test_namedtuple_dict_conversion(self, test_data):
        """Test namedtuple converted to dict."""
        result = evaluate_query(
            "dict(namedtuple('Person', 'name age')('Alice', 30)._asdict())", test_data
        )
        assert result == {"name": "Alice", "age": 30}

    def test_namedtuple_with_data(self, test_data):
        """Test namedtuple with actual data."""
        result = evaluate_query(
            "list(namedtuple('Item', 'name age')(_['items'][0]['name'], _['items'][0]['age']))",
            test_data,
        )
        assert result == ["Alice", 30]


class TestCollectionsIntegration:
    """Test collections module integration with complex queries."""

    def test_counter_filter_combination(self, test_data):
        """Test Counter combined with filtering."""
        result = evaluate_query(
            "Counter(item['active'] for item in _['items'])", test_data
        )
        assert result[True] == 2
        assert result[False] == 1

    def test_defaultdict_grouping(self, test_data):
        """Test defaultdict for grouping data."""
        result = evaluate_query("defaultdict(list)", test_data)
        result["NYC"].append("item1")
        assert "item1" in result["NYC"]

    def test_ordereddict_sorted_integration(self, test_data):
        """Test OrderedDict with sorted data."""
        result = evaluate_query("OrderedDict(sorted(_['metadata'].items()))", test_data)
        assert isinstance(result, OrderedDict)
        assert len(result) == 3

    def test_deque_with_counter(self, test_data):
        """Test deque and Counter combination."""
        result = evaluate_query(
            "list(deque(Counter([1, 2, 2, 3, 3, 3]).elements()))", test_data
        )
        assert result == [1, 2, 2, 3, 3, 3]

    def test_namedtuple_map(self, test_data):
        """Test namedtuple with map function."""
        result = evaluate_query(
            "list(map(lambda x: x.name, [namedtuple('Person', 'name age')(i['name'], i['age']) for i in _['items']]))",
            test_data,
        )
        assert result == ["Alice", "Bob", "Charlie"]
