from database import conexao_banco
from Visual.visual import carregar_pontos_loop, limpar_tela
from Validadores.confirmacao import   confirmacao

def validar_integridade():
    """
    Valida a integridade da votação comparando o total de votos registrados
    na urna com a quantidade de eleitores com status 'Já Votou'.

    Args:
        Nenhum.

    Returns:
        bool: True se a quantidade de votos bater com a quantidade de eleitores que votaram, False caso contrário.
    """

    limpar_tela()

    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM votos")
    total_votos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_votacao = 1")
    total_ja_votou = cursor.fetchone()[0]

    cursor.close()
    conexao.close()

    carregar_pontos_loop(3, "Validando Integridade")

    if total_votos == total_ja_votou:
        print(f"Validação concluída, nenhum voto foi perdido.")
        confirmacao()
        return True
    else:
        print(f"Validação não concluída, possível inconsistência.")
        confirmacao()
        return False