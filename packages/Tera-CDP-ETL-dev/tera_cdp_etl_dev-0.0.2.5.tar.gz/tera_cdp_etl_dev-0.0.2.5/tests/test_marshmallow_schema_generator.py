from tera_etl.validations.marshmallow_schema_generator import generate_schema_marshmallow
import json
import tests.helper_for_test as helper
import os


data_test = {
    "ingestprofile": {
        "DeviceId": "090349324324",
        "UserId": "090349324324",
        "HomePhone": "0369841490",
        "PrimaryPhone": '0369841490',
        "HomeNo": "",
        "StreetName": "",
        "Ward": "15 NGÕ 341, Phường Xuân Phương",
        "District": "Quận Nam Từ Liêm",
        "Province": "Thành phố Hà Nội",
        "Country": "Việt Nam",
        "FirstName": "NGUYỄN THỊ BÍCH ",
        "LastName": "HIỀN",
        "Email": "abc@gmail.com",
        "Gender": "Female",
        "DayofBirth": "19",
        "MonthofBirth": "10",
        "YearofBirth": "1997",
        "Occupation": "IT",
    }
}


def __get_schema_path(schema_name):
    path_data = helper.test_data_folder()
    return os.path.join(path_data,'schema_registry',f'{schema_name}.json')


def test_generate_schema_marshmallow_validate_format_redundant_columns():
    schema_name = 'ingestprofile'
    with open(__get_schema_path(schema_name), 'r') as f:
        new_case_data = data_test[schema_name].copy()
        new_case_data['RedundantKey'] = 'TEST'
        schema_registry = json.loads(f.read())
        GeneratedSchema = generate_schema_marshmallow(schema_registry)
        res = GeneratedSchema().validate(new_case_data)
        assert res == {'RedundantKey': ['Unknown field.']}


def test_generate_schema_marshmallow_validate_format_missing_columns():
    schema_name = 'ingestprofile'
    with open(__get_schema_path(schema_name), 'r') as f:
        new_case_data = data_test[schema_name].copy()
        del new_case_data['UserId']
        schema_registry = json.loads(f.read())
        GeneratedSchema = generate_schema_marshmallow(schema_registry)
        res = GeneratedSchema().validate(new_case_data)
        assert res == {'UserId': ['Missing data for required field.']}


def test_generate_schema_marshmallow_validate_gender():
    schema_name = 'ingestprofile'
    with open(__get_schema_path(schema_name), 'r') as f:
        new_case_data = data_test[schema_name].copy()
        new_case_data['Gender'] = 'TEST'
        schema_registry = json.loads(f.read())
        GeneratedSchema = generate_schema_marshmallow(schema_registry)
        res = GeneratedSchema().validate(new_case_data)
        assert res == {'Gender': ['Must be one of: Male, Female, Other.']}


def test_generate_schema_marshmallow_validate_nullable():
    schema_name = 'ingestprofile'
    with open(__get_schema_path(schema_name), 'r') as f:
        new_case_data = data_test[schema_name].copy()
        new_case_data['FirstName'] = None
        schema_registry = json.loads(f.read())
        GeneratedSchema = generate_schema_marshmallow(schema_registry)
        res = GeneratedSchema().validate(new_case_data)
        assert res == {'FirstName': ['Field may not be null.']}


def test_generate_schema_marshmallow_validate_range():
    schema_name = 'ingestprofile'
    with open(__get_schema_path(schema_name), 'r') as f:
        new_case_data = data_test[schema_name].copy()
        new_case_data['DayofBirth'] = 32
        new_case_data['MonthofBirth'] = 13
        new_case_data['YearofBirth'] = 1919
        schema_registry = json.loads(f.read())
        GeneratedSchema = generate_schema_marshmallow(schema_registry)
        res = GeneratedSchema().validate(new_case_data)
        assert res == {
            'DayofBirth': ['Must be greater than or equal to 1 and less than or equal to 31.'],
            'MonthofBirth': ['Must be greater than or equal to 1 and less than or equal to 12.'],
            'YearofBirth': ['Must be greater than or equal to 1920.']
        }


def test_generate_schema_marshmallow():
    schema_name = 'ingestprofile'
    with open(__get_schema_path(schema_name), 'r') as f:
        new_case_data = data_test[schema_name].copy()
        schema_registry = json.loads(f.read())
        GeneratedSchema = generate_schema_marshmallow(schema_registry)
        res = GeneratedSchema().validate(new_case_data)
        assert res == {}
