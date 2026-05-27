from rich.table import Table

from database import conexao_banco
from Visual.visual import carregar_pontos_loop, limpar_tela
from Validadores.confirmacao import   confirmacao
from rich.console import Console
from rich import box
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
    - Se o total de votos for exatamente igual ao número de eleitores que compareceram, confirma a integridade do pleito e retorna `True`.
    - Se houver qualquer divergência numérica entre as duas contagens, emite um alerta crítico de possível inconsistência/fraude e retorna `False`.

    Args:
        None.

    Returns:
        bool: Retorna True se a validação for bem-sucedida (dados consistentes).
              Retorna False se a base estiver vazia ou se houver divergência entre as contagens.
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

    carregar_pontos_loop(2, "Validando Integridade")

    if total_votos == 0:
        mensagem = "[bold white]Nenhum voto registrado para concluir a validação.[/bold white]"
        cor = "bold white"
    elif total_votos == total_ja_votou:
        mensagem = "[bold green]Validação concluída, nenhum voto foi perdido.[/bold green]"
        cor = "bold spring_green1"
    else:
        mensagem = "[bold red]Validação não concluída, possível inconsistência.[/bold red]"
        cor = "bold red"

    tabela = Table(
        title="Validação de Integridade",
        box=box.DOUBLE,
        border_style=cor,
        title_style="bold bright_white",
        header_style=cor,
        show_lines=True
    )

    tabela.add_column("Total de Votos", justify="center", style="bright_white")
    tabela.add_column("Eleitores que Votaram", justify="center", style="bright_white")
    tabela.add_column("Resultado", justify="center")

    tabela.add_row(str(total_votos), str(total_ja_votou), mensagem)

    console.print(Align.center(tabela))

    confirmacao()