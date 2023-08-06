## Quickstart

### Step 1: Install the data package in your DISPATCHES environment using pip

```sh
conda activate dispatches-dev  # or the name of your DISPATCHES dev environment
pip install git+https://github.com/gmlc-dispatches/dynamic-sweep-data
```

### Step 2: Access the contents of the data package in your code using `dispatches_data.api`

Using `dispatches_data.api.path()`:

```py
from dispatches_data.api import path

# path_to_data_package is a standard pathlib.Path object
path_to_data_package = path("dynamic_sweep")

# subdirectories and files can be accessed using the pathlib.Path API
path_to_NE_results = path_to_data_package / "NE" / "sweep_parameters_results_NE_whole.h5"
assert path_to_NE_results.is_file()

# if the path must be passed to a function that only accepts `str` objects, it can be converted using `str()`
path_to_NE_results_as_str = str(path_to_NE_results)
```

Using `dispatches_data.api.files()`:

```py
from dispatches_data.api import files

# paths_to_all_results_files will be a list of pathlib.Path objects for each file matching the specified `pattern`
paths_to_all_results_files = files("dynamic_sweep", pattern="**/sweep_parameters_results_*_whole.h5")
# check that the list of found files is not empty
assert paths_to_all_results_files

# `dispatches_data.api.files()` always returns a list, even if only one file matches
path_to_NE_results = files("dynamic_sweep", pattern="NE/*result_*_whole.h5")[0]
```

## Examples

### Loading multiple CSV files into a pandas DataFrame

```py
import pandas as pd
from dispatches_data.api import files


def load_data(case_study: str = "NE") -> pd.DataFrame:
    results_file_pattern = f"{case_study}/results_*_sweep_*/*.csv"
    csv_files_to_load = files("dynamic_sweep", pattern=results_files_pattern)
    if not csv_files_to_load:
        raise LookupError("No files found with pattern {results_file_pattern!r}")
    df = pd.concat(
        [pd.read_csv(csv_path) for csv_path in csv_files_to_load],
        axis="index"
    )
    # process df as needed
    return df


def main():
    df_NE = load_data("NE")
    df_RE = load_data("RE")
    ...
```
