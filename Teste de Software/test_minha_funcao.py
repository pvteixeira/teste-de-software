# test_minha_funcao.py

import pytest
from minha_funcao import soma, subtrai, eh_par

# --- Testes Pytest Padrão (São os "Testes de Regressão" quando reexecutados) ---
# O Pytest encontra e roda automaticamente estas funções (que começam com 'test_')

def test_soma_positivos():
    assert soma(2, 3) == 5

def test_soma_negativos():
    assert soma(-1, -5) == -6

def test_soma_zero():
    assert soma(0, 0) == 0

def test_subtrai_simples():
    assert subtrai(5, 2) == 3

def test_subtrai_negativo():
    assert subtrai(2, 5) == -3

def test_eh_par_positivo_par():
    assert eh_par(4) is True

def test_eh_par_positivo_impar():
    assert eh_par(3) is False

def test_eh_par_zero():
    assert eh_par(0) is True

# --- Funções Auxiliares para Testes Personalizados (Chamadas pela GUI) ---
# Estas funções não são testes Pytest automáticos; elas simulam a lógica de teste.

def executar_teste_personalizado_soma(num1, num2, resultado_esperado):
    """
    Executa um teste de soma com valores fornecidos pelo usuário.
    Retorna uma string formatada com o resultado (PASS/FAIL).
    """
    try:
        resultado_real = soma(num1, num2)
        if resultado_real == resultado_esperado:
            return f"[PASS] Soma({num1}, {num2}) == {resultado_esperado} (Real: {resultado_real})"
        else:
            return f"[FAIL] Soma({num1}, {num2}) == {resultado_esperado} (Real: {resultado_real}) - ERRO: Resultado incorreto."
    except Exception as e: # Captura TypeErrors e outros erros
        return f"[FAIL] Soma({num1}, {num2}) - ERRO: {type(e).__name__}: {e}"

def executar_teste_personalizado_subtracao(num1, num2, resultado_esperado):
    """
    Executa um teste de subtração com valores fornecidos pelo usuário.
    Retorna uma string formatada com o resultado (PASS/FAIL).
    """
    try:
        resultado_real = subtrai(num1, num2)
        if resultado_real == resultado_esperado:
            return f"[PASS] Subtrai({num1}, {num2}) == {resultado_esperado} (Real: {resultado_real})"
        else:
            return f"[FAIL] Subtrai({num1}, {num2}) == {resultado_esperado} (Real: {resultado_real}) - ERRO: Resultado incorreto."
    except Exception as e:
        return f"[FAIL] Subtrai({num1}, {num2}) - ERRO: {type(e).__name__}: {e}"

def executar_teste_personalizado_par(numero, resultado_esperado_str):
    """
    Executa um teste de 'eh_par' com valor fornecido pelo usuário.
    resultado_esperado_str é uma string ('True', 'False', '1', '0').
    Retorna uma string formatada com o resultado (PASS/FAIL).
    """
    try:
        # Converte a string de resultado esperado para um booleano
        esperado_bool = False
        if isinstance(resultado_esperado_str, str):
            if resultado_esperado_str.lower() == 'true' or resultado_esperado_str == '1':
                esperado_bool = True
            elif resultado_esperado_str.lower() == 'false' or resultado_esperado_str == '0':
                esperado_bool = False
            else:
                raise ValueError("Resultado esperado para Eh_Par deve ser 'True', 'False', '1' ou '0'.")
        elif isinstance(resultado_esperado_str, (int, float)):
            esperado_bool = bool(resultado_esperado_str) # Converte números como 1/0 para True/False
        else:
            raise TypeError("Tipo de resultado esperado inválido para Eh_Par.")

        resultado_real = eh_par(numero) # Chama a função original eh_par

        if resultado_real == esperado_bool:
            return f"[PASS] Eh_par({numero}) == {resultado_esperado_str} (Real: {resultado_real})"
        else:
            return f"[FAIL] Eh_par({numero}) == {resultado_esperado_str} (Real: {resultado_real}) - ERRO: Resultado incorreto."
    except Exception as e:
        return f"[FAIL] Eh_par({numero}) - ERRO: {type(e).__name__}: {e}"