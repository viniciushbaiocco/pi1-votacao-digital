from database import conexao_banco

def verificar_titulo_de_eleitor_banco(titulo):
    """
    Verifica a existência de um número de título de eleitor na base de dados.

    A função executa uma consulta de contagem (`COUNT(*)`) por correspondência exata
    na tabela de eleitores para identificar se o título informado já possui um cadastro
    ativo. Esta rotina compõe uma das etapas cruciais de validação de presença e de
    vínculo administrativo de mesários nas interfaces da urna.

    O cursor de execução e a conexão de rede aberta com o servidor MySQL são encerrados
    de forma imediata após a recuperação do registro, mitigando o acúmulo de sessões
    ociosas (idle) no banco.

    Args:
        titulo (str): O número do título de eleitor, previamente tratado e validado
            por regras de formato, a ser consultado na tabela.

    Returns:
        tuple: Uma tupla contendo um único número inteiro na primeira posição,
        representando o resultado do COUNT. Retorna `(1,)` se o título de eleitor
        for localizado na base de dados, ou `(0,)` caso contrário.
    """
    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()
    query = "SELECT COUNT(*) FROM eleitores WHERE titulo_eleitor = %s"
    cursor.execute(query, (titulo, ))
    resultado = cursor.fetchone()
    
    cursor.close()
    conexao.close()

    return resultado


