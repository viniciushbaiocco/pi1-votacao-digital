from database import conexao_banco
from Visual.visual import carregar_pontos_loop, limpar_tela
from Validadores.confirmacao import   confirmacao
from rich.console import Console

console = Console(highlight=False)

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
        console.print(f"[bold green]Validação concluída, nenhum voto foi perdido.[/bold green]")
        confirmacao()
        return True
    else:
        console.print(f"[bold red]Validação não concluída, possível inconsistência.[/bold red]")
        confirmacao()
        return False