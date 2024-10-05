import json
import os
import sys
from typing import Any

"""
Called by
python add_field.py gpt4o_Qiskit_qiskit_versions.json  
"""


def add_field_to_json(obj: Any, field_name: str, field_value: Any) -> Any:
    """
    Recursively traverses the JSON object and adds/updates the specified field.

    Parameters:
        obj (Any): The JSON object (dict or list) to traverse.
        field_name (str): The name of the field to add/update.
        field_value (Any): The value to set for the field.

    Returns:
        Any: The modified JSON object.
    """
    if isinstance(obj, dict):
        obj[field_name] = field_value
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                add_field_to_json(value, field_name, field_value)
    elif isinstance(obj, list):
        for item in obj:
            add_field_to_json(item, field_name, field_value)
    return obj


def process_json_file(
    input_path: str, output_path: str = None, overwrite: bool = False
) -> None:
    """
    Reads a JSON file, adds/updates the specified field in every JSON object, and writes the output.

    Parameters:
        input_path (str): Path to the input JSON file.
        output_path (str, optional): Path to save the modified JSON file. If not provided and overwrite is False, defaults to 'output.json'.
        overwrite (bool, optional): If True, overwrites the input file with the modified JSON. Defaults to False.

    Raises:
        FileNotFoundError: If the input file does not exist.
        json.JSONDecodeError: If the input file is not a valid JSON.
        IOError: If there are issues reading or writing files.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            f"The file '{input_path}' does not exist or is not a file."
        )

    try:
        with open(input_path, "r", encoding="utf-8") as infile:
            data = json.load(infile)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON format: {e.msg}", e.doc, e.pos)
    except Exception as e:
        raise IOError(f"Error reading the file '{input_path}': {e}")

    # Add/update the field
    modified_data = add_field_to_json(data, "model_name_or_path", "gpt4o")

    # Determine output path
    if overwrite:
        output_path = input_path
    elif not output_path:
        output_path = "output.json"

    try:
        with open(output_path, "w", encoding="utf-8") as outfile:
            json.dump(modified_data, outfile, indent=4)
        print(f"Modified JSON has been saved to '{output_path}'.")
    except Exception as e:
        raise IOError(f"Error writing to the file '{output_path}': {e}")


def main():
    """
    Parses command-line arguments and processes the JSON file accordingly.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Add 'model_name_or_path': 'gpt4o' to every JSON object in a file."
    )
    parser.add_argument("input_file", help="Path to the input JSON file.")
    parser.add_argument(
        "-o",
        "--output",
        help='Path to save the modified JSON file. Defaults to "output.json" if not specified and overwrite is False.',
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the input file with the modified JSON.",
    )

    args = parser.parse_args()

    try:
        process_json_file(args.input_file, args.output, args.overwrite)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
