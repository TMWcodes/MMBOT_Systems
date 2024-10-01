import json
import os
import pandas as pd
from data_loader import load_json

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '_')
        elif isinstance(x, list):
            out[name[:-1]] = json.dumps(x)  # Store list as JSON string
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def unflatten_json(flat):
    out = {}
    for k, v in flat.items():
        keys = k.split('_')
        d = out
        for key in keys[:-1]:
            if key.isdigit():
                key = int(key)
            if key not in d:
                d[key] = {}
            d = d[key]
        try:
            v = json.loads(v)  # Convert JSON string back to list
        except (ValueError, TypeError):
            pass
        d[keys[-1]] = v
    return out

def json_to_csv(json_filename, csv_filename):
    try:
        data = load_json(json_filename)
        flattened_data = [flatten_json(item) for item in data]

        df = pd.DataFrame(flattened_data)
        
        csv_dir = os.path.dirname(csv_filename)
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)

        df.to_csv(csv_filename, encoding='utf-8', index=False)
        
        print(f"Successfully converted '{json_filename}' to '{csv_filename}'.")

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as ve:
        print(f"Value error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")

# CSV to JSON Function
def csv_to_json(csv_filename, json_filename):
    try:
        df = pd.read_csv(csv_filename, encoding='utf-8')
        data = df.to_dict(orient='records')
        unflattened_data = [unflatten_json(item) for item in data]

        json_dir = os.path.dirname(json_filename)
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(unflattened_data, json_file, indent=4)
        
        print(f"Successfully converted '{csv_filename}' to '{json_filename}'.")

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as ve:
        print(f"Value error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")

