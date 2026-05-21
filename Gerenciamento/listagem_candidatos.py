from database import conexao_banco as conect
from Validadores import confirmacao
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich import box
from Visual.visual import limpar_tela

console = Console(highlight=False)


def listagem_candidatos():
    limpar_tela()

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute('SELECT * FROM candidatos')
        total_candidatos = cursor.fetchall()

        if len(total_candidatos) == 0:
            console.print('\n Nenhum candidato cadastrado no sistema.', style="bold yellow")
        else:
            tabela = Table(
                title="Listagem de Candidatos",
                box=box.DOUBLE,
                border_style="bold sandy_brown",
                title_style="bold bright_white",
                header_style="bold sandy_brown",
                show_lines=True
            )

            tabela.add_column("ID",               justify="center", style="bright_white")
            tabela.add_column("Nome",              style="bright_white")
            tabela.add_column("Partido",           style="bright_white")
            tabela.add_column("Sigla",             justify="center", style="bright_white")
            tabela.add_column("Número de Votação", justify="center", style="bright_white")

            for candidato in total_candidatos:
                tabela.add_row(
                    str(candidato['id']),
                    candidato['nome'],
                    candidato['partido'],
                    candidato['sigla_partido'],
                    candidato['numero_votacao']
                )

            console.print(Align.center(tabela))
            console.print(f'\n Total de Candidatos Cadastrados: [bold white]{len(total_candidatos)}[/bold white]')

    except Exception as erro:
        console.print(f'\n Erro ao listar candidatos: {erro}', style="bold red")

    confirmacao.confirmacao()

    cursor.close()
    conexao.close()
