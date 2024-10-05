import json
import argparse
import os
from typing import Any, Dict, List, Union


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Rename a field in all instances within a JSON file."
    )
    parser.add_argument("input_file", type=str, help="Path to the input JSON file.")
    parser.add_argument(
        "original_field", type=str, help="The field name to be renamed."
    )
    parser.add_argument("new_field", type=str, help="The new field name.")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Path to the output JSON file. If not provided, '_modified' is appended to the input file name.",
    )
    return parser.parse_args()


def rename_field(data: Any, original_field: str, new_field: str) -> Any:
    """
    Recursively traverse the JSON data and rename the specified field.

    Args:
        data: The JSON data (dict, list, or other).
        original_field: The field name to rename.
        new_field: The new field name.

    Returns:
        The modified JSON data with the field renamed.
    """
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            # Rename the key if it matches the original field
            new_key = new_field if key == original_field else key
            # Recursively process the value
            new_dict[new_key] = rename_field(value, original_field, new_field)
        return new_dict
    elif isinstance(data, list):
        return [rename_field(item, original_field, new_field) for item in data]
    else:
        return data


def main():
    args = parse_arguments()

    input_path = args.input_file
    original_field = args.original_field
    new_field = args.new_field
    output_path = args.output

    # Determine the output file path
    if not output_path:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_modified{ext}"

    # Read the input JSON file
    try:
        with open(input_path, "r", encoding="utf-8") as infile:
            data = json.load(infile)
    except FileNotFoundError:
        print(f"Error: The file '{input_path}' was not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from '{input_path}'.\n{e}")
        return

    # Rename the field
    modified_data = rename_field(data, original_field, new_field)

    # Write the modified JSON to the output file
    try:
        with open(output_path, "w", encoding="utf-8") as outfile:
            json.dump(modified_data, outfile, indent=4, ensure_ascii=False)
        print(
            f"Successfully renamed '{original_field}' to '{new_field}' in '{output_path}'."
        )
    except IOError as e:
        print(f"Error: Failed to write to '{output_path}'.\n{e}")


if __name__ == "__main__":
    main()
