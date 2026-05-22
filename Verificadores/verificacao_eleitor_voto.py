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