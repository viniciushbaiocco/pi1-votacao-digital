import time
from Validadores import confirmacao
from database import conexao_banco as cb
from rich.console import Console
from rich.table import Table
from rich import box
from Visual import visual
from rich.align import Align

console = Console(highlight=False)


def votos_por_partido():
    conexao = None
    cursor = None
    try:
        conexao = cb.conexao_banco()
        cursor = conexao.cursor(dictionary=True)

        tabela = Table(
            title="Listagem de votos por partido",
            box=box.DOUBLE,
            border_style="bold sandy_brown",
            title_style="bold bright_white",
            header_style="bold sandy_brown",
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

        visual.carregar_pontos_loop(2, "Consultando Resultados")
        time.sleep(1)
        console.print(Align.center(tabela))
        confirmacao.confirmacao()
        visual.limpar_tela()

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
