import os
import re
import subprocess
from collections import defaultdict, Counter
from tabulate import tabulate
import csv
import ast


def check_type_annotations(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.returns is not None:
                return True
            for arg in node.args.args:
                if arg.annotation is not None:
                    return True
    return False


def analyze_file(directory, file_path, table_data):
    print(f"Analisando o arquivo: {file_path}\n")

    # Verificar Type Annotations
    type_annotations_present = check_type_annotations(file_path)

    # Executar Pylint
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
    # Atualizar a estrutura de dados da tabela
    table_row = [directory, file_path, total_alerts]
    for alert_type in alert_type_names.keys():
        table_row.append(alert_count[alert_type])

    table_row.append(", ".join(sorted(set(alert_code for alert_codes in alert_details.values() for alert_code in alert_codes))))
    table_row.append("Sim" if type_annotations_present else "Não")  # Adiciona o campo "Adota Type Annotations?"

    # Executar Mypy
    mypy_process = subprocess.run(["mypy", file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  universal_newlines=True, check=False)
    mypy_output = mypy_process.stdout

    # Adiciona o campo "Descrição de Type Annotations"
    if type_annotations_present:
        table_row.append(mypy_output.strip())
    else:
        table_row.append("Nenhum")

    table_data.append(table_row)

    print(f"\nO arquivo '{file_path}' {'adota' if type_annotations_present else 'não adota'} Type Annotations.\n")
    print("========================================\n")

    print("\nResultado da análise Mypy:")
    print(mypy_output)

    return total_alerts

def main():
    directory = "test"
    os.chdir(directory)  # Muda o diretório para 'teste'

    table_data = []
    total_alerts_directory = 0

    for file_name in os.listdir():
        if file_name.endswith(".py"):
            total_alerts_directory += analyze_file(directory, file_name, table_data)

    # Adiciona uma linha no final com o total de alertas
    table_data.append(['Total de alertas por diretório', '', total_alerts_directory, '', '', '', '', '', '', '', ''])

    print("Tabela de alertas Pylint:")
    print(tabulate(table_data,
                   headers=["Diretório Analisado", "Arquivo", "Quantidade Total de alertas",
                            "Quantidade de alertas Convention", "Quantidade de alertas Refactor",
                            "Quantidade de alertas Warning", "Quantidade de alertas Error",
                            "Quantidade de alertas Fatal", "Descrição de alertas", "Adota Type Annotations?",
                            "Descrição de Type Annotations"],
                   tablefmt="grid",
                   colalign=("left", "left", "left", "left", "left", "left", "left", "left", "left", "left", "left")))


if __name__ == "__main__":
    main()

