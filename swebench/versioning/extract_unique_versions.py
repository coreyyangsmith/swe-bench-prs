import json
import os
from typing import Any, Set, List


def extract_unique_versions(file_path: str) -> List[str]:
    """
    Extracts all unique values from the 'version' field in a JSON file.

    Parameters:
        file_path (str): The path to the JSON file.

    Returns:
        List[str]: A sorted list of unique 'version' values.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON.
        Exception: For any other unforeseen errors.
    """

    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"The file '{file_path}' does not exist or is not a file."
        )

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON format: {e.msg}", e.doc, e.pos)
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")

    unique_versions: Set[str] = set()

    def traverse(obj: Any):
        """
        Recursively traverses the JSON object to find all 'version' fields.

        Parameters:
            obj (Any): The current JSON object or value.
        """
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "version":
                    if isinstance(value, str):
                        unique_versions.add(value)
                    else:
                        unique_versions.add(str(value))
                else:
                    traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)

    traverse(data)

    return sorted(unique_versions)


# Example Usage
if __name__ == "__main__":
    # Replace 'path_to_your_file.json' with the actual file path
    json_file_path = "gpt4o_Qiskit_qiskit_versions.json"

    try:
        versions = extract_unique_versions(json_file_path)
        print("Unique 'version' values found:")
        for version in versions:
            print(version)
    except Exception as e:
        print(f"Error: {e}")
