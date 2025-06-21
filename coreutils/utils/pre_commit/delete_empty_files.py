import os
import sys
from typing import List


def delete_empty_files(filenames: list[str]) -> list[str]:
    deleted_files: List = []
    for file in filenames:
        if file.endswith(".py") and os.path.isfile(file) and os.path.getsize(file) == 0:
            os.remove(file)
            deleted_files.append(file)
    return deleted_files


def main() -> None:
    filenames: str = sys.argv[1:]
    deleted: bool = delete_empty_files(filenames)

    if deleted:
        for file in deleted:
            print(f"Deleted empty file: {file}")
    sys.exit(0)


if __name__ == "__main__":
    main()
