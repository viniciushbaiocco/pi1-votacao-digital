from database import conexao_banco

def verificar_mesario(titulo, cpf_4_criptografado, chave_acesso_criptografada):
    """
    Verifica se o conjunto de credenciais fornecido pertence a um mesário ativo no banco.

    A função executa uma consulta de contagem (`COUNT(*)`) para validar de forma combinada
    e simultânea três fatores de identidade do mesário. A busca aplica regras rígidas
    de correspondência por igualdade estrita para o título e a chave de acesso, além de
    utilizar a função nativa `SUBSTRING` do MySQL para comparar apenas o fatiamento inicial
    de 4 caracteres da hash do CPF.

    A cláusula `mesario = 1` garante que o acesso seja negado mesmo se os dados estiverem
    corretos, caso o eleitor correspondente não possua a flag de privilégio administrativo
    concedida na base de dados.

    Args:
        titulo (str): O número do título de eleitor já tratado e validado.
        cpf_4_criptografado (str): A hash do CPF do usuário, da qual serão extraídos
            apenas os 4 caracteres iniciais para validação posicional.
        chave_acesso_criptografada (str): A assinatura da chave de acesso pessoal,
            já tratada e criptografada.

    Returns:
        tuple: Uma tupla contendo um único número inteiro na primeira posição,
        representando o resultado do COUNT. Retorna `(1,)` se o conjunto de dados
        corresponder perfeitamente a um mesário habilitado, ou `(0,)` caso contrário.
    """
    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()
    quatro_digitos = cpf_4_criptografado[:4]
    query = """
        SELECT COUNT(*) FROM eleitores
        WHERE titulo_eleitor = %s
        AND SUBSTRING(cpf, 1, 4) = %s
        AND chave_acesso = %s
        AND mesario = 1
    """
    cursor.execute(query, (titulo, quatro_digitos, chave_acesso_criptografada))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado
