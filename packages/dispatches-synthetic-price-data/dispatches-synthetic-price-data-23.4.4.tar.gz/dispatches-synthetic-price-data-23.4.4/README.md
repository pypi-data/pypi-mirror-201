## Quickstart

### Step 1: Install the data package in your DISPATCHES environment using pip

```sh
conda activate dispatches-dev  # or the name of your DISPATCHES dev environment
pip install git+https://github.com/gmlc-dispatches/synthetic-price-data
```

### Step 2: Access the contents of the data package in your code using `dispatches_data.api`

Using `dispatches_data.api.path()`:

```py
from dispatches_data.api import path

# path_to_data_package is a standard pathlib.Path object
path_to_data_package = path("synthetic_price")

# subdirectories and files can be accessed using the pathlib.Path API
path_to_xml = path_to_data_package / "ARMA_train.xml"
assert path_to_xml.is_file()

# alternatively, if the file is located directly under the data package directory (i.e. not in a subdirectory):
# this will raise an exception if the file does not exist so we don't need to check explicitly
path_to_xml = path("synthetic_price", "ARMA_train.xml")

# if the path must be passed to a function that only accepts `str` objects, it can be converted using `str()`
path_to_xml_as_str = str(path_to_xml)
```

Using `dispatches_data.api.files()`:

```py
from dispatches_data.api import files

# `all_price_files` will be a list of pathlib.Path objects for each file matching the specified `pattern`
all_price_files = files("synthetic_price", pattern="Price_20*.csv")
# check that the list of found files is not empty
assert all_price_files

# `dispatches_data.api.files()` always returns a list, even if only one file matches
price_for_21 = files("synthetic_price", pattern="Price_*21.csv")[0]
```

Using the CLI interface:

**NOTE** this example uses UNIX shell syntax. It will not work on Windows unless adapted to the specific shell (e.g. Powershell) being used.

```sh
# calling `dispatches-data-packages` on the command line with the name of the data package
# will output the absolute path to the data package, which can then be saved as a shell variable
# and used to generate paths to files in the data package
path_to_data_package="$(dispatches-data-packages synthetic_price)"
path_to_xml_file="$path_to_data_package/ARMA_train.xml"
ls -lh "$path_to_data_package"
cp "$path_to_xml_file" .

# the entire contents of the data package can be copied to the current working directory
# if this is required by the client application
cp -r "$path_to_data_package"/* .
ls -lh .
```

## Examples

### Using the data package with the RAVEN CLI

**NOTE** this example uses UNIX shell syntax. It will not work on Windows unless adapted to the specific shell (e.g. Powershell) being used.
**TODO**: must be tested

```sh
path_to_data_package="$(dispatches-data-packages synthetic_price)"
# copy contents to local directory
cp -r "$path_to_data_package"/* .
raven_framework ARMA_train.xml
```

### Using the data package with shell commands in IPython/Jupyter notebooks

Both the IPython shell and Jupyter notebooks allow running arbitrary shell commands within a Python code shell by prefixing the command with `!`.
Refer to the [IPython documentation](https://ipython.readthedocs.io/en/stable/interactive/python-ipython-diff.html#shell-assignment) for details.

**NOTE** The command (minus the `!` prefix) is passed verbatim to the system shell. Therefore, the exact syntax used in these examples may or may not work depending on the operating system (more specifically, on which shell is configured as the default).

Within a `!`-prefixed line, the use of Python variables is supported by prefixing the variable name with `$` or wrapping it between `{}`.
The _value_ of the Python variable will be converted to a string automatically before the command is passed to the shell.

Therefore, the following syntax can be used to use data packages within a IPython/Jupyter shell command:

```py
from dispatches_data.api import path

xml_path = path("synthetic_price", "ARMA_train.xml)

# the $ syntax only supports simple variable names
!raven_framework $xml_path

# the {} syntax supports arbitrary Python expressions
!raven_framework {path("synthetic_price", "ARMA_train.xml")}
```
