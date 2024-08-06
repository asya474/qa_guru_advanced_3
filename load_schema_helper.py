import json
import os


def load_schema(filename: str) -> dict:
    schema_dir = os.path.join(os.path.dirname(__file__), "schemas", filename)
    try:
        with open(schema_dir, 'r') as schema:
            return json.loads(schema.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"Schema file '{filename}' not found in '{schema_dir}'.")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON schema file '{filename}': {str(e)}")