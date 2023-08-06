# jQueryQueryBuilder
Python Rule evaluator for jQuery-QueryBuilder. It evaluates rules agains provided objects.

[Website](http://www.shunyeka.com) • [autobotAI Cloud Governance](https://autobot.live/)

Inspired from [SixiS/jquery_query_builder-rails](https://github.com/SixiS/jquery_query_builder-rails)

## Usage

Install the package.

```
pip install jqqb
```

Usage Example:

```python
from jqqb import QueryBuilder
rule_json = {
    "condition": "AND",
    "rules": [{
        "id": "tagname",
        "field": "tags.name",
        "type": "string",
        "input": "text",
        "operator": "not_contains",
        "value": "production"
    }, {
        "id": "tagname",
        "field": "tags.name",
        "type": "string",
        "input": "text",
        "operator": "begins_with",
        "value": "development"
    }, {
        "condition": "OR",
        "rules": [{
            "id": "type",
            "field": "type",
            "type": "string",
            "input": "text",
            "operator": "equal",
            "value": "ec2"
        },{
            "id": "type",
            "field": "type",
            "type": "string",
            "input": "text",
            "operator": "equal",
            "value": "ami"
        }]
    }]
}


evaluator = QueryBuilder(rule_json)
object_1 = {'type': "ec2", "tags": [{"name": "hello"}, {"name": "asdfasfproduction_instance"}]}
object_2 = {'type': "ami", "tags": [{"name": "development"}, {"name": "asfdafdroduction_instance"}, {"name": "proction"}]}
objects = [object_1, object_2]

print(evaluator.match_objects(objects))
print(evaluator.inspect_objects(objects))
```

Result:

```python
[{'type': 'ami', 'tags': [{'name': 'development'}, {'name': 'asfdafdroduction_instance'}, {'name': 'proction'}]}]

[
    {
        'object': {'type': 'ec2', 'tags': [{'name': 'hello'}, {'name': 'asdfasfproduction_instance'}]},
        'selected': False,
        'results': [
            (
                {'id': 'tagname', 'field': 'tags.name', 'type': 'string', 'input': 'text', 'operator': 'not_contains', 'value': 'production'},
                (['hello', 'asdfasfproduction_instance'], 'production', False)
            ),
            (
                {'id': 'tagname', 'field': 'tags.name', 'type': 'string', 'input': 'text', 'operator': 'begins_with', 'value': 'development'},
                (['hello', 'asdfasfproduction_instance'], 'development', False)
            ),
            (
                {
                    'condition': 'OR',
                    'rules': [
                        {
                            'id': 'type',
                            'field': 'type',
                            'type': 'string',
                            'input': 'text',
                            'operator': 'equal',
                            'value': 'ec2'
                        }, {
                            'id': 'type',
                            'field': 'type',
                            'type': 'string',
                            'input': 'text',
                            'operator': 'equal',
                            'value': 'ami'
                        }
                    ]
                },
                [
                    (
                        {'id': 'type', 'field': 'type', 'type': 'string', 'input': 'text', 'operator': 'equal', 'value': 'ec2'},
                        ('ec2', 'ec2', True)
                    ),
                    (
                        {'id': 'type', 'field': 'type', 'type': 'string', 'input': 'text', 'operator': 'equal', 'value': 'ami'},
                        ('ec2', 'ami', False)
                    )
                ]
            )
        ]
    },
    {
        'object': {'type': 'ami', 'tags': [{'name': 'development'}, {'name': 'asfdafdroduction_instance'}, {'name': 'proction'}]},
        'selected': True,
        'results': [
            (
                {'id': 'tagname', 'field': 'tags.name', 'type': 'string', 'input': 'text', 'operator': 'not_contains', 'value': 'production'},
                (
                    ['development', 'asfdafdroduction_instance', 'proction'], 'production', True
                )
            ), (
                {'id': 'tagname', 'field': 'tags.name', 'type': 'string', 'input': 'text', 'operator': 'begins_with', 'value': 'development'},
                (
                    ['development', 'asfdafdroduction_instance', 'proction'], 'development', True
                )
            ), (
                {
                    'condition': 'OR',
                    'rules': [
                        {'id': 'type', 'field': 'type', 'type': 'string', 'input': 'text', 'operator': 'equal', 'value': 'ec2'},
                        {'id': 'type', 'field': 'type', 'type': 'string', 'input': 'text', 'operator': 'equal', 'value': 'ami'}
                    ]
                }, [
                    (
                        {'id': 'type', 'field': 'type', 'type': 'string', 'input': 'text', 'operator': 'equal', 'value': 'ec2'},
                        ('ami', 'ec2', False)
                    ), (
                        {'id': 'type', 'field': 'type', 'type': 'string', 'input': 'text', 'operator': 'equal', 'value': 'ami'},
                        ('ami', 'ami', True)
                    )
                ]
            )
        ]
    }
]
```

## Run tests

```bash
python setup.py test
```
