# rw_dataframe_data_io

`rw_dataframe_data_io` is a Python library for reading and writing files of different formats, such as CSV, JSON, and Pickle. It provides a simple interface for reading and writing data from these files.

## Installation

To install `rw_dataframe_data_io`, run the following command: `pip install rw-dataframe-data-io`


## Usage

### The `file_rw()` function

The main function of `file_rw` is `file_rw()`, which allows you to read or write data from files. Here are the available parameters:

* `file_path`: The path to the file.
* `data`: The data to write to the file. Can be a Pandas DataFrame, Pandas series, or any other Python object.
* `mode`: The mode in which to open the file. Can be "read" or "write".
* `sep`: The separator for CSV files.
* `file_extension`: The file extension. Can be "csv", "json", or "pkl".
* `parent_directory`: The parent directory in which to save the file. Can be None to save in the current directory.
* `serie`: If True, the function reads a CSV file to return a Pandas series.
* `use_cols`: The column to select for reading the series. If None, all columns are read.
* `column_name`: The column names for the DataFrame. If None, default column names will be used.

### Examples

Read a CSV file:

```python
from utils import file_rw

data = file_rw("data.csv")
print(data)
```
Write a CSV file:

```python
from utils import file_rw
import pandas as pd

data = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
file_rw("data.csv", data=data, mode="write")
```
Read a JSON file:

```python
from utils import file_rw

data = file_rw("data.json", file_extension="json")
print(data)
```
Write a JSON file:

```python
from utils import file_rw
import pandas as pd

data = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
file_rw("data.json", data=data, mode="write", file_extension="json")
```
Read a Pickle file:

```python
from utils import file_rw

data = file_rw("data.pkl", file_extension="pkl")
print(data)
```
Write a Pickle file:

```python
from utils import file_rw
import pandas as pd

data = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
file_rw("data.pkl", data=data, mode="write", file_extension="pkl")

```

## Contribution

Contributions are welcome! To contribute to file_rw, please create a pull request with your proposed changes.


