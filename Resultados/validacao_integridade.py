from rich.table import Table

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
    Valida a integridade matemática da eleição cruzando dados de votos e eleitores.

    A função atua como uma ferramenta de auditoria interna da urna eleitoral. Ela realiza
    duas consultas independentes no banco de dados MySQL:

    1. Conta o volume total de cédulas eletrônicas armazenadas na tabela `votos`.
    2. Conta o quantitativo de eleitores que possuem o status de votação ativo (`status_votacao = 1`).

    A partir dessas métricas, valida o ecossistema sob três cenários lógicos:
    - Se não houver registros de votos, aborta a validação retornando `False`.
    - Se o total de votos for exatamente igual ao número de eleitores que compareceram,
      confirma a integridade do pleito e retorna `True`.
    - Se houver qualquer divergência numérica entre as duas contagens, emite um alerta
      crítico de possível inconsistência/fraude e retorna `False`.

    Args:
        None.

    Returns:
        bool: Retorna True se a validação for bem-sucedida (dados consistentes).
              Retorna False se a base estiver vazia ou se houver divergência entre as contagens.
    """

    limpar_tela()

    # Estabelece a conexão usando o módulo do projeto [cite: 201]
    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM votos")
    total_votos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_votacao = 1")
    total_ja_votou = cursor.fetchone()[0]

    cursor.close()
    conexao.close()

    carregar_pontos_loop(2, "Validando Integridade")

    tabela = Table(
        title="Validação de Integridade",
        box=box.DOUBLE,
        border_style="bold sandy_brown",
        title_style="bold bright_white",
        header_style="bold sandy_brown",
        show_lines=True
    )

    tabela.add_column("Total de Votos", justify="center", style="bright_white")
    tabela.add_column("Eleitores que Votaram", justify="center", style="bright_white")

    tabela.add_row(str(total_votos), str(total_ja_votou))

    console.print(Align.center(tabela))

    if total_votos == 0:
        console.print(Panel(Align.center("[bold yellow]Nenhum voto registrado para concluir a validação.[/bold yellow]"),
                            title="[bold bright_white]Validação de Integridade[/bold bright_white]",
                            border_style="bold spring_green1", box=box.DOUBLE, padding=(1, 4)))
        confirmacao()
        return False

    elif total_votos == total_ja_votou:
        console.print(Panel(Align.center("[bold green]Validação concluída, nenhum voto foi perdido.[/bold green]"),
                            title="[bold bright_white]Validação de Integridade[/bold bright_white]",
                            border_style="bold spring_green1", box=box.DOUBLE, padding=(1, 4)))
        confirmacao()
        return True

    else:
        console.print(Panel(Align.center("[bold red]Validação não concluída, possível inconsistência.[/bold red]"),
                            title="[bold bright_white]Validação de Integridade[/bold bright_white]", border_style="bold red",
                            box=box.DOUBLE, padding=(1, 4)))
        confirmacao()
        return False