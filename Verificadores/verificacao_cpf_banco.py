
"""
    Solicita o CPF validado e criptografado para consulta no banco de dados.

    Args:
        mensagem(str): entrar com um CPF validado e criptografado.

    Returns:
        mensagem(str): Retorna se há eleitor cadastrado com o CPF no banco de dados ou não.

    """


def verificar_cpf_banco(cpf_criptografado):
    from database import conexao_banco
    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()
    query = "SELECT COUNT(*) FROM eleitores WHERE cpf = %s"
    cursor.execute(query, (cpf_criptografado, ))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado
# entender com o grupo se deixa o return no resultado com 0/1 ou mensagem


# Teste da funcao
if __name__ == "__main__":
    cpf = str(input("CPF: "))
    result = verificar_cpf_banco(cpf)
    print(result)
