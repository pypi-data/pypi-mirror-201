from enum import Enum
from tera_etl.validations.marshmallow_schema_generator import generate_schema_marshmallow


class QualityControlResult(Enum):
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'


def classify_data(data_chunk, schema_registry, **kwargs) -> dict:
    is_accepted = __is_accepted(data_chunk, schema_registry)
    return {
        "qc_type": QualityControlResult.ACCEPTED if is_accepted["status"] else QualityControlResult.REJECTED,
        "errors": is_accepted["errors"]
    }


def __is_accepted(chunk, schema_registry):
    return __has_valid_schema(chunk, schema_registry)


def __has_valid_schema(data, schema_registry):
    GeneratedSchema = generate_schema_marshmallow(schema_registry)
    errors = GeneratedSchema().validate(data)
    return {
        "status": True if not errors else False,
        "errors": errors,
    }
