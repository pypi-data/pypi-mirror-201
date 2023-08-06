# Function: polish_file(input_file, output_file, exceptions='')

This function takes in an input file and an output file, both with supported file extensions (.csv, .json, or .txt), and an optional list of exceptions.

## Parameters
- `input_file` (`str`): The path to the input file to be polished.
- `output_file` (`str`): The path to the output file to be written with the polished data.
- `exceptions` (`str`, optional): An optional string of characters to be excluded from the polishing process.

## Returns
- `None`

## Raises
- `Exception`: If the input and output files do not have the same supported file extension.
- `Exception`: If the file format is not supported.

## Supported file extensions
- `.csv`: Comma-separated values file
- `.json`: JavaScript Object Notation file
- `.txt`: Text file

## Description
This function cleans the input file by removing impurities, such as special characters, except for those included in the optional exceptions list. The cleaned data is then written to the output file with the same format as the input file.

**Note:** This function does not check if the input file exists or if the output file can be written to. It is the responsibility of the calling code to ensure that the necessary file permissions and file paths are valid.

```python
# Import the function
from pypolish import polish

# Define the input and output files
input_file = "data/input.json"
output_file = "data/output.json"

# Define any exceptions to the cleaning process
exceptions = ['(', '.', '@']


polish.polish_file(input_file, output_file, exceptions)

# Check the output file to see if the cleaning process was successful
with open(output_file, 'r') as f:
    print(f.read())
```

##Github Repo
https://github.com/huntert1004/pypolish