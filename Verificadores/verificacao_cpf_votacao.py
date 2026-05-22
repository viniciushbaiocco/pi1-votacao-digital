from database import conexao_banco

def verificar_cpf_voto(cpf_criptografado):
    """
    Verifica a existência de um eleitor com base no fragmento inicial do CPF criptografado.

    A função extrai uma fatia contendo os 4 primeiros caracteres da hash de CPF informada
    e realiza uma busca de contagem (`COUNT(*)`) no banco de dados. A consulta utiliza a
    função nativa `SUBSTRING` do MySQL para comparar apenas o início da string gravada na
    tabela de eleitores, atuando como o primeiro fator de identificação no terminal de voto.

    O cursor e a conexão aberta com o servidor MySQL são devidamente encerrados após a
    captura do resultado, garantindo a liberação imediata dos recursos de rede.

    Args:
        cpf_criptografado (str): A hash completa do CPF do eleitor, da qual serão
            extraídos os 4 primeiros caracteres para a validação por fatiamento.

    Returns:
        tuple: Uma tupla contendo um único número inteiro na primeira posição,
        representando o resultado do COUNT. Retorna `(1,)` se algum eleitor possuir a
        mesma assinatura inicial na coluna de CPF, ou `(0,)` caso contrário.
    """

    # Pega os primeiros quatros dígitos
    quatro_digitos = cpf_criptografado[:4]

    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()

    # Comando em sql que verifica os primeiros 4 dígitos
    query = "SELECT COUNT(*) cpf FROM eleitores WHERE SUBSTRING(cpf, 1, 4) = %s"
    cursor.execute(query, (quatro_digitos,))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado
