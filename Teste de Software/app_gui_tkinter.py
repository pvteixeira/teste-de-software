# app_gui_tkinter.py

import tkinter as tk # IMPORTANTE: Garante que 'tk' esteja definido
from tkinter import scrolledtext, messagebox, ttk
import pytest
import json
import os
import io
import sys
import threading

# Importa as funções auxiliares para testes personalizados
from test_minha_funcao import (
    executar_teste_personalizado_soma,
    executar_teste_personalizado_subtracao,
    executar_teste_personalizado_par
)

def run_all_pytest_tests(output_widget):
    """
    Executa todos os testes Pytest padrão e atualiza o widget de saída.
    """
    output_widget.delete(1.0, tk.END) # Limpa a saída anterior
    output_widget.insert(tk.END, 'Rodando testes padrão (Pytest)... aguarde...\n')
    output_widget.update_idletasks() # Força a atualização visual

    json_report_path = 'pytest_report.json'
    
    # Remove o arquivo de relatório JSON anterior, se existir
    if os.path.exists(json_report_path):
        os.remove(json_report_path)

    # Redireciona a saída padrão para um StringIO para evitar poluir o console
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        # Executa o pytest e gera o relatório JSON
        # O exit_code pode ser 0 (sucesso), 1 (falhas), 2 (erro de uso), etc.
        pytest_exit_code = pytest.main(['-v', '--json-report', f'--json-report-file={json_report_path}', 'test_minha_funcao.py'])
    finally:
        sys.stdout = old_stdout # Restaura a saída padrão

    results_lines = []
    if os.path.exists(json_report_path):
        with open(json_report_path, 'r') as f:
            report_data = json.load(f)
        
        passed_count = 0
        failed_count = 0
        
        for item in report_data.get('test_results', []):
            test_name = item.get('nodeid', 'N/A').split('::')[-1] # Pega só o nome da função do teste
            outcome = item.get('outcome', 'N/A')
            
            if outcome == 'passed':
                passed_count += 1
                results_lines.append(f"[PASS] {test_name}")
            elif outcome == 'failed':
                failed_count += 1
                error_message = ""
                # Tenta pegar a mensagem de erro (pode estar em 'call', 'setup' ou 'teardown')
                if 'call' in item and 'longrepr' in item['call']:
                    error_message = item['call']['longrepr']
                elif 'setup' in item and 'longrepr' in item['setup']:
                     error_message = item['setup']['longrepr']
                elif 'teardown' in item and 'longrepr' in item['teardown']:
                     error_message = item['teardown']['longrepr']

                # Pega apenas a primeira linha do erro para não poluir demais a GUI
                formatted_error = error_message.splitlines()[0] if error_message else 'N/A'
                results_lines.append(f"[FAIL] {test_name}\n   Erro: {formatted_error}")
            else:
                results_lines.append(f"[SKIP] {test_name} ({outcome})") # Exibe outros outcomes como skip, xfail, etc.
        
        total_tests = len(report_data.get('test_results', []))
        summary = f"--- Resumo dos Testes Padrão (Pytest) ---\nTotal: {total_tests}, Passou: {passed_count}, Falhou: {failed_count}\n"
        
        output_widget.insert(tk.END, summary + "\n".join(results_lines))
    else:
        output_widget.insert(tk.END, "Erro: Relatório Pytest JSON não encontrado. Verifique se 'pytest-json-report' está instalado e se os testes foram executados com sucesso.")
    
    # Se Pytest.main() retornou 1 (falhas), pode indicar que o pytest-json-report não funcionou direito
    if pytest_exit_code != 0 and not os.path.exists(json_report_path):
        output_widget.insert(tk.END, "\nAVISO: Pytest retornou um erro e o relatório JSON não foi gerado. Verifique o terminal para mais detalhes do Pytest.")


def start_pytest_thread(output_widget):
    """
    Inicia a execução dos testes Pytest em uma thread separada para não travar a GUI.
    """
    thread = threading.Thread(target=run_all_pytest_tests, args=(output_widget,))
    thread.start()

def run_custom_test(operation, entry1_widget, entry2_widget_or_none, entry_expected_widget, output_widget):
    """
    Executa um teste personalizado com base na operação e entradas do usuário.
    entry2_widget_or_none é o widget para o segundo número (ou None para eh_par).
    """
    output_widget.delete(1.0, tk.END) # Limpa a saída anterior
    output_widget.insert(tk.END, f'Executando teste personalizado de {operation}...\n')
    output_widget.update_idletasks()

    try:
        num1_str = entry1_widget.get().strip() # .strip() remove espaços extras
        expected_str = entry_expected_widget.get().strip()
        num2_str = entry2_widget_or_none.get().strip() if entry2_widget_or_none else None # Pega o valor se o widget existir

        # Validação básica de entrada para evitar ValueError
        if not num1_str:
            raise ValueError("O campo 'Número 1' não pode estar vazio.")
        if operation != "eh_par" and not num2_str:
             raise ValueError("O campo 'Número 2' não pode estar vazio para Soma/Subtração.")
        if not expected_str:
            raise ValueError("O campo 'Resultado Esperado' não pode estar vazio.")

        # --- Processamento para eh_par ---
        if operation == "eh_par":
            try:
                num1 = int(num1_str) # eh_par geralmente espera int
            except ValueError:
                raise ValueError("Para 'Eh_Par', o número deve ser um inteiro.")
            
            # Chama a função auxiliar do test_minha_funcao.py
            result_message = executar_teste_personalizado_par(num1, expected_str)
            
        # --- Processamento para Soma e Subtração ---
        else:
            try:
                # Tenta converter para float se tiver ponto decimal, senão int
                num1 = float(num1_str) if '.' in num1_str else int(num1_str)
                num2 = float(num2_str) if '.' in num2_str else int(num2_str)
                expected = float(expected_str) if '.' in expected_str else int(expected_str)
            except ValueError:
                raise ValueError("Por favor, insira números válidos nos campos.")

            if operation == "soma":
                result_message = executar_teste_personalizado_soma(num1, num2, expected)
            elif operation == "subtracao":
                result_message = executar_teste_personalizado_subtracao(num1, num2, expected)
            else:
                result_message = "[ERRO] Operação personalizada desconhecida."
        
        output_widget.insert(tk.END, result_message + "\n")

    except ValueError as ve:
        output_widget.insert(tk.END, f"[ERRO DE ENTRADA] {ve}\n")
    except Exception as e:
        output_widget.insert(tk.END, f"[ERRO INESPERADO] Ocorreu um problema: {type(e).__name__}: {e}\n")


# --- Configuração da Janela Principal ---
root = tk.Tk()
root.title("App de Testes - Personalizável")
root.geometry("750x700") # Aumentando um pouco mais a altura
root.resizable(False, False) # Impede redimensionamento para manter o layout fixo

# --- Frame para os Testes Padrão ---
standard_tests_frame = tk.LabelFrame(root, text="Testes Padrão (Regressão)", padx=15, pady=10)
standard_tests_frame.pack(pady=10, padx=15, fill="x")

run_all_button = tk.Button(standard_tests_frame, text="Rodar TODOS os Testes Padrão (Pytest)", font=('Helvetica', 12, 'bold'),
                            command=lambda: start_pytest_thread(output_text))
run_all_button.pack(pady=5)

# --- Separador ---
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x', padx=15, pady=10)

# --- Frame para Testes Personalizados ---
custom_tests_frame = tk.LabelFrame(root, text="Testes Personalizados (Entrada do Usuário)", padx=15, pady=10)
custom_tests_frame.pack(pady=10, padx=15, fill="x")

# Grid para organizar os campos e botões
custom_tests_frame.columnconfigure(1, weight=1) # Faz a coluna dos Entrys se expandir

# Linha 0: Número 1
tk.Label(custom_tests_frame, text="Número 1:", font=('Helvetica', 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_num1 = tk.Entry(custom_tests_frame, width=20, font=('Helvetica', 10))
entry_num1.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
soma_button = tk.Button(custom_tests_frame, text="Testar Soma", font=('Helvetica', 10),
                        command=lambda: run_custom_test("soma", entry_num1, entry_num2, entry_expected_soma_sub, output_text))
soma_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

# Linha 1: Número 2
tk.Label(custom_tests_frame, text="Número 2:", font=('Helvetica', 10)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_num2 = tk.Entry(custom_tests_frame, width=20, font=('Helvetica', 10))
entry_num2.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
sub_button = tk.Button(custom_tests_frame, text="Testar Subtração", font=('Helvetica', 10),
                       command=lambda: run_custom_test("subtracao", entry_num1, entry_num2, entry_expected_soma_sub, output_text))
sub_button.grid(row=1, column=2, padx=10, pady=5, sticky="ew")


# Linha 2: Resultado Esperado (para Soma/Subtração)
tk.Label(custom_tests_frame, text="Esperado (Soma/Sub.):", font=('Helvetica', 10)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_expected_soma_sub = tk.Entry(custom_tests_frame, width=20, font=('Helvetica', 10))
entry_expected_soma_sub.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Linha 3: Eh_Par - Número
tk.Label(custom_tests_frame, text="Número (Eh_Par):", font=('Helvetica', 10)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_eh_par_num = tk.Entry(custom_tests_frame, width=20, font=('Helvetica', 10))
entry_eh_par_num.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
eh_par_button = tk.Button(custom_tests_frame, text="Testar Eh_Par", font=('Helvetica', 10),
                          command=lambda: run_custom_test("eh_par", entry_eh_par_num, None, entry_expected_eh_par, output_text))
eh_par_button.grid(row=3, column=2, padx=10, pady=5, sticky="ew")

# Linha 4: Eh_Par - Resultado Esperado
tk.Label(custom_tests_frame, text="Esperado (Eh_Par True/False):", font=('Helvetica', 10)).grid(row=4, column=0, padx=5, pady=5, sticky="w")
entry_expected_eh_par = tk.Entry(custom_tests_frame, width=20, font=('Helvetica', 10))
entry_expected_eh_par.grid(row=4, column=1, padx=5, pady=5, sticky="ew")


# --- Área de Saída Principal para Resultados ---
output_text = scrolledtext.ScrolledText(root, width=80, height=15, font=('Courier New', 10), bg='#F0F0F0', fg='black')
output_text.pack(pady=10, padx=15, fill="both", expand=True)

# --- Botão Sair ---
exit_button = tk.Button(root, text="Sair", font=('Helvetica', 10), command=root.destroy)
exit_button.pack(pady=10)

root.mainloop()