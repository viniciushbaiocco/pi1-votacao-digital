from database import conexao_banco

def verificar_titulo_de_eleitor_banco(titulo):
    """
    Verifica a existência de um título de eleitor no banco de dados.

    Args:
        titulo(str): O título de eleitor validado a ser consultado no banco de dados.

    Returns:
        tuple: Uma tupla contendo a contagem de eleitores encontrados com o título fornecido.
               Retorna (1,) se o título for encontrado, (0,) caso contrário.
    """
    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()
    query = "SELECT COUNT(*) FROM eleitores WHERE titulo_eleitor = %s"
    cursor.execute(query, (titulo, ))
    resultado = cursor.fetchone()
    
    cursor.close()
    conexao.close()

    return resultado


