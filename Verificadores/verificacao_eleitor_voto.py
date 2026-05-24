from database import conexao_banco as conect

def verificacao_eleitor_voto (chave_acesso_criptografada):
    """
    Consulta o banco de dados para verificar se o eleitor associado à chave já votou.

    Esta função realiza uma busca pontual na tabela de eleitores utilizando a assinatura
    criptografada da chave de acesso como filtro. Ela recupera o valor booleano ou inteiro
    armazenado na coluna `status_votacao`, permitindo que o sistema identifique se o cidadão
    está apto a votar ou se a sessão deve bloquear uma tentativa de reautenticação.

    Os recursos de rede, cursores e conexões com o banco MySQL são encerrados de forma
    imediata após a recuperação do registro para evitar overhead de sessões abertas.

    Args:
        chave_acesso_criptografada (str): A hash da chave de acesso, devidamente tratada
            e criptografada, utilizada como identificador único na busca pelo registro.

    Returns:
        tuple: Uma tupla contendo o valor da coluna consultada na primeira posição.
        Retorna `(1,)` caso o eleitor correspondente já tenha computado o voto,
        ou `(0,)` caso contrário (eleitor ainda apto a votar).
    """

    conexao = conect.conexao_banco()
    cursor = conexao.cursor()
    query = "SELECT status_votacao FROM eleitores WHERE chave_acesso = %s"
    cursor.execute(query, (chave_acesso_criptografada,))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado


def verificar_identidade_eleitor(titulo, cpf_4_criptografado, chave_acesso_criptografada):
    """
    Verifica, em uma única consulta, se título + 4 dígitos do CPF + chave pertencem ao mesmo eleitor.

    Espelha a lógica de `Verificadores.verificacao_mesario_banco` (sem o filtro `mesario = 1`),
    comparando os três fatores na MESMA linha da tabela. Isso impede que credenciais de
    eleitores diferentes (CPF de um, título de outro, chave de um terceiro) passem combinadas.

    Args:
        titulo (str): O número do título de eleitor já tratado e validado.
        cpf_4_criptografado (str): A hash do CPF, da qual se usam os 4 primeiros caracteres.
        chave_acesso_criptografada (str): A hash da chave de acesso pessoal.

    Returns:
        tuple: Uma tupla com a contagem na primeira posição. `(1,)` se a identidade
        confere integralmente, `(0,)` caso contrário.
    """
    conexao = conect.conexao_banco()
    cursor = conexao.cursor()
    quatro_digitos = cpf_4_criptografado[:4]
    query = """
        SELECT COUNT(*) FROM eleitores
        WHERE titulo_eleitor = %s
        AND SUBSTRING(cpf, 1, 4) = %s
        AND chave_acesso = %s
    """
    cursor.execute(query, (titulo, quatro_digitos, chave_acesso_criptografada))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado