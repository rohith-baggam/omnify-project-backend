#!/usr/bin/env python3

import ast
import os
import sys
from collections import defaultdict
from typing import List, Dict

# Root directory to start scanning
PROJECT_DIR: str = os.getcwd()

# Files to scan
PYTHON_FILE_EXTENSIONS: tuple[str, ...] = (".py",)


def find_classes_in_file(filepath: str) -> List[str]:
    """
    Extract class names from a Python file, excluding 'Meta' class.
    :param filepath: Path to the Python file to parse.
    :return: A list of class names found in the file, excluding 'Meta'.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        try:
            node: ast.Module = ast.parse(
                file.read(), filename=filepath
            )  # type hint for AST node
        except SyntaxError:
            return []

    # Extract class names, but exclude 'Meta'
    return [
        n.name
        for n in ast.walk(node)
        if isinstance(n, ast.ClassDef) and n.name not in ["Meta", "Command"]
    ]


def scan_project_for_classes() -> Dict[str, List[str]]:
    """
    Scan the entire project directory for classes and map class names to their file locations.
    :return: A dictionary where keys are class names and values are lists of file paths where the class is found.
    """
    class_map: Dict[str, List[str]] = defaultdict(list)

    for root, _, files in os.walk(PROJECT_DIR):
        # Optional: skip migrations or virtual environments
        if "migrations" in root or "venv" in root or "__pycache__" in root:
            continue

        for file in files:
            if file.endswith(PYTHON_FILE_EXTENSIONS):
                # type hint for filepath (str)
                filepath: str = os.path.join(root, file)
                class_names: List[str] = find_classes_in_file(
                    filepath
                )  # type hint for class_names (List[str])
                for name in class_names:
                    class_map[name].append(filepath)

    return class_map


def main() -> None:
    """
    Main function to check for duplicate class names in the project.
    If duplicates are found, block the commit; otherwise, allow it.
    """
    duplicates_found: bool = False  # type hint for duplicates_found (bool)
    class_map: Dict[str, List[str]] = scan_project_for_classes()

    for class_name, locations in class_map.items():
        if len(locations) > 1:
            duplicates_found: bool = True
            print(f"\nDuplicate class name found: '{class_name}'")
            for loc in locations:
                print(f"  - {loc}")
        # if len(locations) > 1:
        #     duplicates_found: bool = True
        #     print(f"\nDuplicate class name found: '{class_name}'")
        #     for loc in locations:
        #         print(f"  - {loc}")

    if duplicates_found:
        print("\nCommit blocked due to duplicate class names.")
        sys.exit(1)
    else:
        print("No duplicate class names found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
