from marshmallow import Schema, fields
from marshmallow.validate import Regexp, Length, OneOf, Range
import os
import json


def __parse_validate_to_marshmallow_format(validates_condition):
    validate = []
    for validate_item in validates_condition:
        key, value = list(validate_item.items())[0]
        if key == 'regex':
            validate.append(
                Regexp(fr"{value}")
            )
        elif key == 'choices':
            validate.append(
                OneOf(value.split('|'))
            )
        elif key == 'range':
            validate.append(
                Range(
                    min=__str_to_number(value.split('-')[0]),
                    max=__str_to_number(value.split('-')[1]),
                    min_inclusive=True,
                    max_inclusive=True,
                )
            )
        elif key == 'min':
            validate.append(
                Range(
                    min=__str_to_number(value),
                    min_inclusive=True,
                )
            )
        elif key == 'max':
            validate.append(
                Range(
                    max=__str_to_number(value),
                    max_inclusive=True,
                )
            )
        elif key == 'gt':
            validate.append(
                Range(
                    min=__str_to_number(value),
                    min_inclusive=False,
                )
            )
        elif key == 'lt':
            validate.append(
                Range(
                    max=__str_to_number(value),
                    max_inclusive=False,
                )
            )
        else:
            raise Exception(f'Unimplement this case "{key}:{value}"')
    return validate


def __str_to_number(str_number):
    return int(str_number) if str_number.isdigit() else float(str_number)


def __mapping_type_marshmallow(data_type, nullable, validate, required=True):
    switcher = {
        'INT': fields.Int(
            required=required,
            allow_none=nullable,
            validate=validate
        ),
        'STRING': fields.Str(
            required=required,
            allow_none=nullable,
            validate=validate
        ),
        'FLOAT': fields.Float(
            required=required,
            allow_none=nullable,
            validate=validate
        ),
        'DATETIME': fields.DateTime(
            required=required,
            allow_none=nullable,
            validate=validate
        ),
    }
    if data_type not in switcher:
        raise Exception(f'Unimplement this data type {data_type}')
    return switcher[data_type]


def generate_schema_marshmallow(schema_registry):
    arg_fields = {}
    for field in schema_registry['Structures']['Fields']:
        validate = __parse_validate_to_marshmallow_format(field['Validation'])
        arg_fields[field['Name']] = __mapping_type_marshmallow(
            data_type=field['FieldType'].upper(),
            nullable=field['Nullable'],
            validate=validate,
        )
    generated_schema = Schema.from_dict(arg_fields)
    return generated_schema
