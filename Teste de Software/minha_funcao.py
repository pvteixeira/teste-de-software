# minha_funcao.py

def soma(a, b):
    """
    Retorna a soma de dois números.
    """
    # Exemplo de um erro que você pode simular para testar o FAIL:
    # if a == 1 and b == 1:
    #     return 3 # Isso fará o teste de soma(1,1) falhar
    return a + b

def subtrai(a, b):
    """
    Retorna a subtração de dois números.
    """
    return a - b

def eh_par(numero):
    """
    Verifica se um número é par.
    """
    # Garante que a entrada é um número inteiro, caso contrário levanta um erro
    if not isinstance(numero, (int, float)):
        raise TypeError("A entrada para 'eh_par' deve ser um número.")
    return numero % 2 == 0