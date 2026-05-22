from database import conexao_banco

def verificar_cpf_banco(cpf_criptografado):
    """
    Verifica a existência da hash de um CPF na base de dados de eleitores.

    A função executa uma consulta de contagem (`COUNT(*)`) por igualdade estrita na
    tabela de eleitores para identificar se o CPF mascarado e criptografado informado
    já possui um cadastro ativo no sistema. Essa checagem serve como uma das barreiras
    de validação multifator para liberar o terminal de votação.

    O cursor e a conexão aberta com o servidor MySQL são encerrados logo após a captura
    do resultado, garantindo a liberação imediata dos recursos de rede do banco.

    Args:
        cpf_criptografado (str): A hash do CPF, previamente tratada e criptografada,
            a ser consultada na tabela de eleitores.

    Returns:
        tuple: Uma tupla contendo um único número inteiro na primeira posição,
        representando o resultado do COUNT. Retorna `(1,)` se o CPF correspondente
        for localizado na base de dados, ou `(0,)` caso contrário.
    """
    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()
    query = "SELECT COUNT(*) FROM eleitores WHERE cpf = %s"
    cursor.execute(query, (cpf_criptografado, ))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado



