# Financial Data Validator

## Overview

The Financial Data Validator(Validata) is a Python tool designed to validate and repair financial datasets. It applies various validation rules to ensure data integrity and provides suggestions for fixing identified issues. This tool is particularly useful for those who work intimately with time-series data.

## Features

- **Validation Rules**: Implements multiple validation rules to check for common data issues, such as price spikes and timestamp monotonicity.
- **Repair Mode**: Suggests fixes for identified data issues, such as interpolating missing price points.
- **Command-Line Interface**: Easily run validations and repairs from the command line.

## Installation

A python virtual environment will need to be created:
```
python3 -m venv .venv
source .venv/bin/activate
```

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To validate a dataset, use the following command:

```
python src/cli.py validate --input <input_file> --threshold <threshold_percent>
```

To run the tool in repair mode, use:

```
python src/cli.py repair --input <input_file>
```

## Examples

### Validating Data

```bash
python src/cli.py validate --input sample_data.json --threshold 0.10
```

### Repairing Data

```bash
python src/cli.py repair --input sample_data.json
```

## Testing

To run the tests, use:

```
pytest
```

This will execute all unit tests defined in the `tests` directory, ensuring that both the validation and repair functionalities work as expected.
