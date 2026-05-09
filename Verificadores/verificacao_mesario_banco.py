from database import conexao_banco

def verificar_mesario(titulo, cpf_4_criptografado, chave_acesso_criptografada):
    """
    Verifica se o título de eleitor, os 4 primeiros dígitos do CPF e a chave de acesso
    correspondem a um mesário cadastrado no banco de dados.

    Args:
        titulo (str): Título de eleitor validado.
        cpf_4_criptografado (str): Primeiros 4 dígitos do CPF criptografados.
        chave_acesso_criptografada (str): Chave de acesso criptografada.

    Returns:
        tuple: Retorna (1,) se os dados correspondem a um mesário, (0,) caso contrário.
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
