import unittest

from jqqb import QueryBuilder


class TestCreateQueryBuilderInstance(unittest.TestCase):
    def setUp(self) -> None:
        self.json_entry = {
            "condition": "AND",
            "rules": [
                {
                    "operator": "equal",
                    "inputs": [
                        {"field": "dummy_key1", "type": "string"},
                        {"type": "string", "value": "dummy_value"}
                    ],
                },
                {
                    "aggregator": "ALL",
                    "field": "dummy_key2",
                    "rule": {
                        "operator": "greater",
                        "inputs": [
                            {"field": "dummy_key3", "type": "integer"},
                            {"type": "integer", "value": 3}
                        ],
                    }
                },
                {
                    "condition": "OR",
                    "rules": [
                        {
                            "aggregator": "ANY",
                            "field": "dummy_key2",
                            "rule": {
                                "operator": "equal",
                                "inputs": [
                                    {"field": "dummy_key3", "type": "integer"},
                                    {"type": "integer", "value": 3}
                                ],
                            }
                        },
                        {
                            "operator": "equal",
                            "inputs": [
                                {"field": "dummy_key4", "type": "boolean"},
                                {"type": "boolean", "value": True}
                            ],
                        }
                    ]
                }
            ]
        }
        return super().setUp()

    def test_create_query_builder_instance_from_json(self):
        query_builder = QueryBuilder.create_from_json(
            json_entry=self.json_entry
        )

        self.assertIsInstance(query_builder, QueryBuilder)


class TestQueryBuilderEvaluate(unittest.TestCase):
    def setUp(self) -> None:
        self.json_entry = {
            "condition": "OR",
            "rules": [
                {
                    "operator": "equal",
                    "inputs": [
                        {"field": "dummy_key1", "type": "string"},
                        {"type": "string", "value": "dummy_value"}
                    ]
                },
                {
                    "aggregator": "ALL",
                    "field": "dummy_key2",
                    "rule": {
                        "operator": "greater",
                        "inputs": [
                            {"field": "dummy_key3", "type": "integer"},
                            {"type": "integer", "value": 3}
                        ]
                    }
                },
                {
                    "condition": "AND",
                    "rules": [
                        {
                            "aggregator": "ANY",
                            "field": "dummy_key2",
                            "rule": {
                                "operator": "equal",
                                "inputs": [
                                    {"field": "dummy_key3", "type": "integer"},
                                    {"type": "integer", "value": 3}
                                ]
                            }
                        },
                        {
                            "operator": "equal",
                            "inputs": [
                                {"field": "dummy_key4", "type": "boolean"},
                                {"type": "boolean", "value": True}
                            ]
                        }
                    ]
                }
            ]
        }
        self.query_builder = QueryBuilder.create_from_json(
            json_entry=self.json_entry
        )
        return super().setUp()

    def test_query_builder_object_matches_rules(self):
        object = {
            "dummy_key1": "other_dummy_value",
            "dummy_key2": [{"dummy_key3": 0}, {"dummy_key3": 3}],
            "dummy_key4": True
        }
        result = self.query_builder.object_matches_rules(object=object)

        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    def test_query_builder_object_does_not_match_rules(self):
        object = {
            "dummy_key1": "other_dummy_value",
            "dummy_key2": [{"dummy_key3": 0}, {"dummy_key3": 3}],
            "dummy_key4": False
        }
        result = self.query_builder.object_matches_rules(object=object)

        self.assertIsInstance(result, bool)
        self.assertFalse(result)


class TestObjectMissingKeyIsSameAsNoneValue(unittest.TestCase):
    def setUp(self) -> None:
        self.json_entry = {
            "condition": "AND",
            "rules": [
                {
                    "operator": "equal",
                    "inputs": [
                        {"field": "dummy_key1", "type": "string"},
                        {"type": "string", "value": None}
                    ]
                },
                {
                    "operator": "equal",
                    "inputs": [
                        {"field": "dummy_key2", "type": "string"},
                        {"type": "string", "value": None}
                    ]
                },
                {
                    "operator": "equal",
                    "inputs": [
                        {"field": "dummy_key1", "type": "string"},
                        {"field": "dummy_key2", "type": "string"}
                    ]
                }
            ]
        }
        self.query_builder = QueryBuilder.create_from_json(
            json_entry=self.json_entry
        )
        return super().setUp()

    def test_query_builder_object_matches_rules_missing_key_are_same_as_None_value(
            self
        ):
        object = {"dummy_key1": None}
        result = self.query_builder.object_matches_rules(object=object)

        self.assertIsInstance(result, bool)
        self.assertTrue(result)
