from jsonschema.validators import validator_for as _validator_for
from jsonschema.protocols import Validator
from jsonschema import validate, ValidationError  # Leave these here so other modules can use them.
from . import jsonschema


def compile(schema: str | dict) -> Validator:
    """Returns the correct validator for the given schema."""
    return _validator_for(schema)(schema)


WSTL_ACTION_SCHEMA_VALIDATOR = compile(jsonschema.WSTL_ACTION_SCHEMA)
WSTL_SCHEMA_VALIDATOR = compile(jsonschema.WSTL_SCHEMA)
CJ_TEMPLATE_SCHEMA_VALIDATOR = compile(jsonschema.CJ_TEMPLATE_SCHEMA)
NVPJSON_SCHEMA_VALIDATOR = compile(jsonschema.NVPJSON_SCHEMA)
