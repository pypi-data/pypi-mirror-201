"""
JSON schemas for validation.
"""
from pkgutil import get_data
from json import loads


def _get_json_schema(schema_file: str) -> str:
    data = get_data(__package__, schema_file)
    assert data is not None, f'Schema file {schema_file} not loaded'
    return loads(data)


WSTL_ACTION_SCHEMA = _get_json_schema('jsonschemas/wstlaction.json')

WSTL_SCHEMA = _get_json_schema('jsonschemas/wstl.json')

CJ_TEMPLATE_SCHEMA = _get_json_schema('jsonschemas/cjtemplate.json')

NVPJSON_SCHEMA = _get_json_schema('jsonschemas/nvpjson.json')
