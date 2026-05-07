from database import conexao_banco as conect

def verificacao_eleitor_voto (chave_acesso_criptografada):
    """
    Verifica se o eleitor já votou ou não pelo banco de dados.

    Args:
        chave_acesso_criptografada(str):A chave de acesso criptografado e validada a ser consultado no banco de dados.

    Returns:
        tupla: Uma tupla dizendo se o eleitor já votou ou não
                Retorna (1,) Já votou, (0,) Caso contrário.
    """

    conexao = conect.conexao_banco()
    cursor = conexao.cursor()
    query = "SELECT status_votacao FROM eleitores WHERE chave_acesso = %s"
    cursor.execute(query, (chave_acesso_criptografada,))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado