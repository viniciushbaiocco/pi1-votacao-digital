from database import conexao_banco

def verificar_cpf_voto(cpf_criptografado):
    """
        Verifica a existência de um cpf (Pega apenas os 4 primeiros dígitos) já criptografado e validado
        do eleitor no banco de dados.

        Args:
            cpf(str): O cpf criptografado e validado a ser consultado no banco de dados.

        Returns:
            tupla: Uma tupla contendo a contagem de eleitores encontrados com o cpf fornecido.
                   Retorna (1,) se o cpf for encontrado, (0,) caso contrário.
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
