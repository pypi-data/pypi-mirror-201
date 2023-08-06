import os

from pathlib import Path
from dependence.function_write import *
from dependence.function_read import *
from dependence.control_folder_exist import *

__all__ = [
    "file_rw",
           ]


def file_rw(file_path, data=None, mode='read', sep=',', file_extension='csv', parent_directory=None, serie=False,
            column_name=None, use_cols=None):
    """
    A function to read or write data to a file. Supports CSV, JSON, and Pickle file formats.

    Parameters:
    ----------
    file_path : str
        The path to the file.
    data : pandas.DataFrame or pandas.Series or any Python object, optional
        The data to be written to the file, by default None.
    file_extension : str, optional
        The file format, either 'csv', 'json', or 'pkl', by default 'csv'.
    mode : str, optional
        The mode in which the file is opened, either 'read' or 'write', by default 'read'.
    parent_directory : str, optional
        allows to save in a specific folder, by default None
    serie: bool = False,
        Read a csv to return a Pandas series
    use_col: Type[str] = None
        If the parameter "serie" is true, allows to select the column to read. If None, all columns will be read.
    column_name: list or None, optional
        A list of new column names for the DataFrame, by default None.
    Returns:
    -------
    pandas.DataFrame or pandas.Series or any Python object
        The data read from the file.
    """
    directory = "dataset"
    if parent_directory is None:
        folder_path = Path(f"{directory}/data_{file_extension}")
        file_root = f"{directory}/data_{file_extension}/{file_path}.{file_extension}"
    else:
        folder_path = Path(parent_directory)
        os.makedirs(parent_directory, exist_ok=True)
        file_root = f"{parent_directory}/{file_path}.{file_extension}"

    if not folder_path.exists():
        print("the path to the file does not exist, create the destination.")
        folder_path.mkdir(parents=True, exist_ok=True)

    file_path = Path(file_root)

    if mode == 'read':
        if file_extension == 'csv':
            if serie:
                usecols = [use_cols] if use_cols else None
                return read_csv(file_path, sep=sep, column_names=column_name, use_cols=usecols, squeeze=True)
            return read_csv(file_path, sep=sep, column_names=column_name)
        elif file_extension == 'json':
            return read_json(file_path)
        elif file_extension == 'pkl':
            return read_pickle(file_path)
        else:
            print("error extension file")
    elif mode == 'write':
        if file_extension == 'csv':
            return write_csv(file_path, data=data, sep=sep, column_names=column_name)
        elif file_extension == 'json':
            return write_json(file_path, data=data)
        elif file_extension == 'pkl':
            return write_pickle(file_path, data=data)
        else:
            print("error extension file")
    else:
        raise ValueError("'mode' must be either 'read' or 'write'")
