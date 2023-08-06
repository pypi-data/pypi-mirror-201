# Pysmells

A Python code analysis tool that checks for programming errors, inconsistencies, and programming style violations, as well as the correctness of type annotations in programs. The pysmells tool is based on the following Python Enhancement Proposals (PEPs): PEP 8, PEP 20, PEP 257, PEP 484, PEP 526, PEP 544, PEP 561, PEP 563, and PEP 589.

## Installation

You can install pysmells using pip:

`pip install pysmells`

## Usage

To use pysmells, navigate to the directory containing the Python files you want to analyze and run the following command:

`pysmells`


pysmells will analyze the Python files in the current directory, checking for programming errors, inconsistencies, programming style violations, and the correctness of type annotations in programs. It will then generate a report detailing the results of the analysis.

## Dependencies

pysmells requires the following packages:

- tabulate
- mypy
- pylint

These dependencies will be automatically installed when you install pysmells using pip.

## License

pysmells is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
