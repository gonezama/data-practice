import os


def list_files_by_extension(directory: str, extension=".csv"):
    """
    Generator that yields all .csv file paths under the given directory.

    Parameters:
        directory (str): Root directory to search

    Yields:
        str: Full path to each CSV file found
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extension):
                yield os.path.join(root, file)


def list_csv_files(directory: str):
    return list(list_files_by_extension(directory))
