def verificar_titulo_de_eleitor_banco(titulo):
    """
    Solicita o título validado para consulta no banco de dados.

    Args:
        mensagem(str): entrar com um título validado.

    Returns:
        mensagem(str): Retorna se há eleitor cadastrado com o título no banco de dados ou não.

    """
    from database import conexao_banco
    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()
    query = "SELECT COUNT(*) FROM eleitores WHERE titulo_eleitor = %s"
    cursor.execute(query, (titulo, ))

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado


# Teste da funcao
if __name__ == "__main__":
    titulo_eleitor = str(input("Título de eleitor: "))
    result = verificar_titulo_de_eleitor_banco(titulo_eleitor)
    print(result)
