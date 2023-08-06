import tera_etl.transform.csv_to_json as csvjson
import tests.helper_for_test as helper
import json
import pytest


def test_convert_csv_to_json():
    data_source = 'test'
    event_name = 'init_data'
    output_path = f'{helper.output_file_path()}/{data_source}_{event_name}.json'
    try:
        csvjson.convert_csv_to_json(data_source, event_name, f'{helper.test_data_folder()}/user_profile_sample.csv')
        with open(output_path, 'r') as f:
            converted = json.load(f)
            assert len(converted) == 5
            assert converted[0]['EventId'] == f"{data_source}_{event_name}_202201439160"
            assert converted[4]['EventId'] == f"{data_source}_{event_name}_202201439163"
            assert converted[0]['UserId'] == 202201439160
            assert converted[4]['UserId'] == 202201439163

            assert converted[0]['HomePhone'] == '0918992678'
            assert converted[4]['HomePhone'] == 'nullnullnull'

            assert converted[0]['Address']['HouseNo'] == ''
    except Exception as e:
        pytest.fail(f'Exception happens {e}')
    finally:
        helper.delete_file(output_path)



def test_hyundai_convert_csv_to_json():
    data_source = 'VTVHyundai'
    event_name = 'IngestProfile'
    output_path = f'{helper.output_file_path()}/{data_source}_{event_name}.json'
    try:
        csvjson.convert_csv_to_json(data_source, event_name, f'{helper.test_data_folder()}/data_customer.csv')
        with open(output_path, 'r') as f:
            converted = json.load(f)
            assert len(converted) > 100
            assert converted[0]['EventId'] == f"{data_source}_{event_name}_202201439160"
            assert converted[4]['EventId'] == f"{data_source}_{event_name}_202201439163"
            assert converted[0]['UserId'] == 202201439160
            assert converted[4]['UserId'] == 202201439163

            assert converted[0]['HomePhone'] == '0918992678'
            assert converted[4]['HomePhone'] == 'nullnullnull'

            assert converted[0]['Address']['HouseNo'] == ''
    except Exception as e:
        pytest.fail(f'Exception happens {e}')
    # finally:
    #     helper.delete_file(output_path)
