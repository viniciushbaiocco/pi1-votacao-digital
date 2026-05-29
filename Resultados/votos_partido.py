import time
from Validadores import confirmacao
from database import conexao_banco as cb
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from Visual.visual import limpar_tela
from rich.align import Align


console = Console(highlight=False)


def votos_por_partido():
    """
    Gera e exibe um relatório consolidado com o total de votos de cada legenda partidária.

    A função consulta o banco de dados MySQL realizando um agrupamento relacional
    (`LEFT JOIN` combinado com `GROUP BY`) entre as tabelas de candidatos e votos.
    Ela contabiliza o volume total de votos recebidos por todos os candidatos pertencentes
    a cada partido e ordena o resultado de forma decrescente (`DESC`), destacando as
    legendas mais votadas no topo.

    As informações coletadas são renderizadas em uma tabela estilizada e centralizada
    no console via biblioteca Rich. O encerramento dos cursores e conexões com a base
    de dados é mapeado de forma segura dentro do bloco `finally`, prevenindo conexões
    pendentes no servidor em caso de interrupções.

    Args:
        None.

    Returns:
        None: A função tem propósito puramente consultivo e de saída visual na CLI.
    """
    conexao = None
    cursor = None
    try:
        conexao = cb.conexao_banco()
        cursor = conexao.cursor(dictionary=True)

        tabela = Table(
            title="Listagem de votos por partido",
            box=box.DOUBLE,
            border_style="bold #D4620A",
            title_style="bold bright_white",
            header_style="bold #D4620A",
            show_lines=True
        )

        tabela.add_column("Partido", style="bright_white")
        tabela.add_column("Sigla Partido", style="bright_white")
        tabela.add_column("Total de Votos", justify="center", style="bright_white")

        query_votos_partido = ("SELECT c.partido, c.sigla_partido, COUNT(v.id_candidato) as total_votos "
                                "FROM candidatos c "
                                "LEFT JOIN votos v "
                                "ON c.id = v.id_candidato "
                                "GROUP BY c.partido, c.sigla_partido "
                                "ORDER BY total_votos DESC;")

        cursor.execute(query_votos_partido)
        votos_partido = cursor.fetchall()

        for partidos in votos_partido:
            tabela.add_row(
                partidos['partido'],
                partidos['sigla_partido'],
                str(partidos['total_votos'])
            )
        
        limpar_tela()
        console.print(Panel(
            Align.center(
                "[bold bright_white]Consultando votos por partido...[/bold bright_white]\n"
                "[dim]Agregando resultados das legendas partidárias.[/dim]"
            ),
            title="[bold bright_white]CONSULTANDO RESULTADOS[/bold bright_white]",
            border_style="bold green",
            box=box.DOUBLE,
            padding=(1, 4)
        ))
        time.sleep(2)
        limpar_tela()
        console.print(Align.center(tabela))
        confirmacao.confirmacao()
        limpar_tela()

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
