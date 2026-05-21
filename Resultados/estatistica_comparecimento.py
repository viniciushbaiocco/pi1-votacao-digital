from database.conexao_banco import conexao_banco
from Visual.visual import carregar_pontos_loop, limpar_tela
from Validadores.confirmacao import   confirmacao
from rich.console import Console
from rich.table import Table
from rich import box, style
from rich.align import Align

console = Console(highlight=False)

def exibir_estatistica_comparecimento() -> None:
    """
    Consulta o banco de dados e exibe no terminal a estatística.

    Args:
        None
    Returns:
        None
    """

    limpar_tela()

    conexao = conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    # Total de eleitores cadastrados
    cursor.execute("SELECT COUNT(*) AS total FROM eleitores")
    total_eleitores = cursor.fetchone()["total"]

    carregar_pontos_loop(3, "Calculando Estatísticas")

    if total_eleitores == 0:
        console.print("\n  [bold red][AVISO] Nenhum eleitor cadastrado no sistema.[/bold red]")
        cursor.close()
        conexao.close()
        return

    # Total de eleitores que votaram (status_votacao = TRUE)
    cursor.execute(
        "SELECT COUNT(*) AS votaram FROM eleitores WHERE status_votacao = TRUE"
    )
    total_votaram = cursor.fetchone()["votaram"]

    cursor.close()
    conexao.close()

    # Cálculo do percentual de comparecimento
    nao_votaram = total_eleitores - total_votaram
    percentual = (total_votaram / total_eleitores) * 100
    percentual_ausencia = (nao_votaram / total_eleitores) * 100

    # Tabela
    tabela = Table(
        title="Estastíticas de Comparecimento",
        box=box.DOUBLE,
        border_style="bold sandy_brown",
        title_style="bold bright_white",
        header_style="bold sandy_brown",
        show_lines=True
    )

    tabela.add_column("Total de Eleitores Aptos", style="bright_white")
    tabela.add_column("Eleitores Que Votaram", style="bright_white")
    tabela.add_column("Eleitores Ausentes", style="bright_white")
    tabela.add_column("Percentual de Comparecimento", style="bright_white")
    tabela.add_column("Percentual de abstenção", style="bright_white")

    tabela.add_row(
        str(total_eleitores),
        str(total_votaram),
        str(nao_votaram),
        f"{percentual:.1f}%",
        f"{percentual_ausencia:.1f}%"
    )

    # Exibição dos resultados
    console.print(Align.center(tabela))

    confirmacao()