
def verificar_cpf_banco(cpf_criptografado):
    """
    Verifica a existência de um cpf já criptografado e validado do eleitor no banco de dados.

    Args:
        cpf(str): O cpf criptografado e validado a ser consultado no banco de dados.

    Returns:
        tupla: Uma tupla contendo a contagem de eleitores encontrados com o cpf fornecido.
               Retorna (1,) se o cpf for encontrado, (0,) caso contrário.
    """
    from database import conexao_banco
    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()
    query = "SELECT COUNT(*) FROM eleitores WHERE cpf = %s"
    cursor.execute(query, (cpf_criptografado, ))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado

print(verificar_cpf_banco("PBLYS725RH1Z"))

