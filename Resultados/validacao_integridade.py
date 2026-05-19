from database import conexao_banco

def validar_integridade():
    """
    Valida a integridade da votação comparando o total de votos registrados
    na urna com a quantidade de eleitores com status 'Já Votou'.

    Args:
        Nenhum.

    Returns:
        bool: True se a quantidade de votos bater com a quantidade de eleitores que votaram, False caso contrário.
    """
    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM votos")
    total_votos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_votacao = 1")
    total_ja_votou = cursor.fetchone()[0]

    cursor.close()
    conexao.close()

    if total_votos == total_ja_votou:
        print(f"Validação concluída, nenhum voto foi perdido.")
        return True
    else:
        print(f"Validação não concluída, possível inconsistência.")
        return False