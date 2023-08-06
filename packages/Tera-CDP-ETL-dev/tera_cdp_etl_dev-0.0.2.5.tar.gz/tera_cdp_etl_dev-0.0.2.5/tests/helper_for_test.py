import os
import tera_etl

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def output_file_path():
    dir_path = f'{tera_etl.root}/tera_etl/output'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


def test_data_folder():
    return f'{tera_etl.root}/tests/data'
