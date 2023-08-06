import os
import re
import subprocess
from collections import Counter, defaultdict
from tabulate import tabulate


def check_type_annotations(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    type_annotation_pattern = re.compile(r'(?<=:)\s*([a-zA-Z_][a-zA-Z0-9_]*|\s*List\s*\[[a-zA-Z0-9_, ]+\])\s*')
    match = type_annotation_pattern.search(content)
    return bool(match)


def analyze_file(directory, file_path, table_data):
    print(f"Analyzing the file: {file_path}\n")

    # Check Type Annotations
    type_annotations_present = check_type_annotations(file_path)

    # Run Pylint
    process = subprocess.run(["pylint", file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             universal_newlines=True, check=False)
    pylint_output = process.stdout

    alert_count = Counter()
    alert_details = defaultdict(list)

    alert_pattern = re.compile(r'([CRWEF]\d{4})')

    alert_type_names = {
        'C': 'Convention',
        'R': 'Refactor',
        'W': 'Warning',
        'E': 'Error',
        'F': 'Fatal'
    }

    for line in pylint_output.split("\n"):
        match = alert_pattern.search(line)
        if match:
            alert_code = match.group(0)
            alert_type = alert_code[0]
            alert_count[alert_type] += 1
            alert_details[alert_type].append(alert_code)

    total_alerts = sum(alert_count.values())
    # Update the table data structure
    table_row = [directory, file_path, total_alerts]
    for alert_type in alert_type_names.keys():
        table_row.append(alert_count[alert_type])

    table_row.append(", ".join(sorted(set(alert_code for alert_codes in alert_details.values() for alert_code in alert_codes))))
    table_row.append("Yes" if type_annotations_present else "No")  # Adds the "Adopt Type Annotations?" field

    # Run Mypy
    mypy_process = subprocess.run(["mypy", file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  universal_newlines=True, check=False)
    mypy_output = mypy_process.stdout

    table_row.append(mypy_output if type_annotations_present else "None")  # Adds the "Type Annotations Description" field
    table_data.append(table_row)

    print(f"\nFile '{file_path}' {'adopts' if type_annotations_present else 'does not adopt'} Type Annotations.\n")
    print("========================================\n")

    print("\nMypy analysis result:")
    print(mypy_output)

    return total_alerts


def main():
    root_directory = input("Enter the directory path containing the Python files to analyze: ")

    table_data = []
    total_alerts_directory = 0

    for root, dirs, files in os.walk(root_directory):
        for file_name in files:
            if file_name.endswith(".py"):
                file_path = os.path.join(root, file_name)
                total_alerts_directory += analyze_file(root, file_path, table_data)

    print(f"\nTotal alerts found in the directory: {total_alerts_directory}\n")
    print(tabulate(table_data, headers=["Directory", "File",
                                        "Total Alerts", "Convention", "Refactor",
                                        "Warning", "Error", "Fatal", "Alert Codes",
                                        "Adopt Type Annotations?",
                                        "Type Annotations Description"],
                   tablefmt="grid"))

if __name__ == "__main__":
    main()
