"""
# marshalDecoder README

## Overview
PycDecompiler is a Python script designed to decompile Python bytecode files (`.pyc`). It utilizes the `pycdc` tool to perform the decompilation.

## Prerequisites
- Python 3.x
- The `pycdc` tool should be available in the same directory as this script.

## Usage
1. Clone or download the repository.
2. Place the target `.py` file written by marshal in the same directory as the script.
3. Open a terminal and navigate to the script's directory.

### Command Syntax
```bash
python marshalDecoder.py -f <input_file.pyc> -o <output_file.py>
```

### Example
```bash
python marshalDecoder.py -f example.py -o output.py
```

Replace `example.py` with the name of your input `.py` file and `output.py` with the desired output file name.

## Notes
- The script uses the `marshalDecoder` class to encapsulate the functionality.
- The `get_magic_code`, `run_bash`, `create_pyc_file`, and `decompile_and_save` methods handle specific tasks.
- The `if __name__ == "__main__":` block initializes an instance of the class and executes the necessary operations.
"""
