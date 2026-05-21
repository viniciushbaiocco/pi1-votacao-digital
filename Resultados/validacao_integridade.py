from database import conexao_banco
from Visual.visual import carregar_pontos_loop, limpar_tela
from Validadores.confirmacao import   confirmacao
from rich.console import Console
from rich import box
from rich.panel import Panel
from rich.align import Align

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
        console.print(Panel(Align.center(f"[bold green]Validação concluída, nenhum voto foi perdido.[/bold green]"), title="[bold bright_white]Validação de Integridade[/bold bright_white]", border_style="bold spring_green1", box=box.DOUBLE, padding=(1, 4)))
        confirmacao()
        return True
    else:
        console.print(Panel(Align.center(f"[bold red]Validação não concluída, possível inconsistência.[/bold red]"), title="[bold bright_white]Validação de Integridade[/bold bright_white]", border_style="bold red", box=box.DOUBLE, padding=(1, 4)))
        confirmacao()
        return False