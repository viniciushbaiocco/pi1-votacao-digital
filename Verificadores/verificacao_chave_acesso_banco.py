from database import conexao_banco

def verificar_chave_acesso_banco(chave_acesso_criptografada):
    """
    Verifica a existência de uma hash de chave de acesso na base de dados de eleitores.

    A função realiza uma consulta de contagem (`COUNT(*)`) na tabela de eleitores para
    identificar se a assinatura criptografada fornecida já consta em algum registro ativo.
    Esta checagem é fundamental para os fluxos de validação de presença, impedindo o
    acesso de chaves inexistentes ou duplicadas no terminal.

    Ao término da execução da consulta, as conexões de rede e os cursores com o servidor
    MySQL são imediatamente desalocados para evitar vazamento de recursos.

    Args:
        chave_acesso_criptografada (str): A hash da chave de acesso, já tratada e
            criptografada, a ser consultada por igualdade no banco de dados.

    Returns:
        tuple: Uma tupla contendo um único número inteiro na primeira posição,
        representando o resultado do COUNT. Retorna `(1,)` se a chave de acesso correspondente
        for localizada no banco de dados, ou `(0,)` caso contrário.
"""
    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()
    query = "SELECT COUNT(*) FROM eleitores WHERE chave_acesso = %s"
    cursor.execute(query, (chave_acesso_criptografada,))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado
