from database import conexao_banco

def verificar_chave_acesso_banco(chave_acesso_criptografada):

    """
    Verifica a existência de uma chave de acesso já criptografada e validada do eleitor no banco de dados.

    Args:
        chave_acesso_criptografada(str):A chave de acesso criptografado e validada a ser consultado no banco de dados.

    Returns:
        tupla: Uma tupla contendo a contagem de eleitores encontrados com a chave de acesso fornecida.
               Retorna (1,) se a chave de acesso for encontrada, (0,) caso contrário.
    """

    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()
    query = "SELECT COUNT(*) FROM eleitores WHERE chave_acesso = %s"
    cursor.execute(query, (chave_acesso_criptografada,))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado
