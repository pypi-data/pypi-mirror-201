import json
import pandas
import os
import sys
from datetime import datetime as d


output_dir = root = os.path.dirname(os.path.abspath(__file__)) + '/../output'


def convert_csv_to_json(data_source, event_name, data_path, number_of_process_lines=-1):
    formatted_data = []
    df = pandas.read_csv(data_path, header=0)
    columns = df.columns
    df.reset_index()

    process_lines = sys.maxsize if number_of_process_lines == -1 else number_of_process_lines
    for index, row in df.iterrows():
        data_obj = {}
        if index >= process_lines:
            break

        id_fields = []
        for col in columns:
            cell = row[col]
            # Case of Pd.na or nan or cell is empty
            if pandas.isna(cell) or pandas.isnull(cell) or not cell:
                data_obj[col] = None
                continue

            lower_col = col.lower()
            
            if 'id' in lower_col:
                id_fields.append(str(cell))
            if 'email' in lower_col:
                # for testing purpose, ignore the email
                continue


            if isinstance(cell, str):
                try:
                    if cell[0] == '{':
                        data_obj[col] = json.loads(cell.replace("'", '"'))
                        continue
                    if cell[0] == '[':
                        # ignore the emails
                        continue
                    data_obj[col] = cell
                except:
                    data_obj[col] = cell
            else:
                data_obj[col] = cell
            
            if col in data_obj and data_obj[col] and 'date' in col.lower() :
                data_obj[col] = d.strftime(d.strptime(data_obj[col], '%Y-%m-%d'), '%Y-%m-%dT%H:%M:%S.%SZ')
            if 'status' in lower_col:
                data_obj[col] = str(data_obj[col])
        data_obj['EventId'] = f'{data_source}_{event_name}_{"".join(id_fields)}'
        formatted_data.append(data_obj)

    
    with open(f'{output_dir}/{data_source}_{event_name}.json', 'w+') as f:
        f.write(json.dumps(formatted_data, ensure_ascii=False, indent=4))
