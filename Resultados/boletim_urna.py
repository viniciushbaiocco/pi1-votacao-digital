import time

from Menu import sub_menus
from database import conexao_banco
from Validadores import confirmacao, gerenciador_de_entrada
from Visual import visual
from rich.console import Console
from rich.table import Table
from rich import box
from rich.align import Align
from rich.panel import Panel

console = Console(highlight=False)

def exibir_boletim_urna():
    """
    Gerencia a interface interativa de apuração e emissão do Boletim de Urna (BU).

    A função se conecta à base de dados para extrair e consolidar os dados das tabelas
    de candidatos e votos. Apresenta um menu interativo que permite duas operações:

    1. Listagem Geral: Realiza um agrupamento (`LEFT JOIN` com `COUNT`) para listar
       todos os candidatos da base e seus respectivos totais de votos em ordem alfabética.
    2. Determinação do Vencedor: Verifica se há votos registrados em sistema e, em
       caso positivo, executa uma consulta ordenada de forma decrescente para retornar
       o candidato com maior volume de votos computados.

    As tabelas de relatórios e painéis de erro são centralizados e renderizados via Rich.
    Independentemente do sucesso ou cancelamento do fluxo, o encerramento seguro dos
    cursores e conexões abertas com o MySQL é sempre garantido pelo bloco `finally`.

    Args:
        None.

    Returns:
        None: A função atua apenas na leitura, agregação e exibição visual de dados no console.
    """
    conexao = None
    cursor = None
    try:
        conexao = conexao_banco.conexao_banco()
        cursor = conexao.cursor(dictionary=True)

        executando_entrada = 1
        while executando_entrada == 1:
            sub_menus.exibir_menu_boletim_urna()
            escolha = gerenciador_de_entrada.obter_entrada_inteira_valida("Escolha uma opção: ", 1, 2)

            tabela = Table(
                title="Listagem de Candidatos",
                box=box.DOUBLE,
                border_style="bold sandy_brown",
                title_style="bold bright_white",
                header_style="bold sandy_brown",
                show_lines=True
            )

            tabela.add_column("Nome", style="bright_white")
            tabela.add_column("Partido", style="bright_white")
            tabela.add_column("Total de Votos", justify="center", style="bright_white")

            tabela_vencedor = Table(
                title="Vencedor",
                box=box.DOUBLE,
                border_style="bold sandy_brown",
                title_style="bold bright_white",
                header_style="bold sandy_brown",
                show_lines=True
            )

            tabela_vencedor.add_column("Nome", style="bright_white")
            tabela_vencedor.add_column("Partido", style="bright_white")
            tabela_vencedor.add_column("Total de Votos", justify="center", style="bright_white")

            match escolha:
                # Opção 1: Listar todos os candidatos com seus votos
                case 1:
                    visual.limpar_tela()
                    query_listagem_candidatos = ('SELECT c.nome, c.partido, '
                                                 'COUNT(v.id) AS total_votos '
                                                 'FROM candidatos c '
                                                 'LEFT JOIN votos v '
                                                 'ON c.id = v.id_candidato '
                                                 'GROUP BY c.id, c.nome, c.partido '
                                                 'ORDER BY nome ASC')

                    cursor.execute(query_listagem_candidatos)
                    total_candidatos = cursor.fetchall()

                    for candidatos in (total_candidatos):
                        tabela.add_row(
                            candidatos['nome'],
                            candidatos['partido'],
                            str(candidatos['total_votos'])
                        )

                    console.print(Align.center(tabela))
                    confirmacao.confirmacao()
                    visual.limpar_tela()

                # Opção 2: Exibir o vencedor da eleição
                case 2:
                    query_verificar_tabela_votos = ('SELECT * FROM votos')
                    cursor.execute(query_verificar_tabela_votos)
                    verificar_tabela = cursor.fetchall()

                    visual.carregar_pontos_loop(3, "Verificando Vencedor")
                    time.sleep(1)

                    if not verificar_tabela:
                        console.print(Panel(Align.center("[bold red]Nenhum Voto Registrado.[/bold red]"), title="[bold bright_white]Erro[/bold bright_white]", border_style="bold red", box=box.DOUBLE, padding=(1, 4)))
                        console.print(Panel(Align.center("[bold yellow]Não foi possível determinar um vencedor.[/bold yellow]"), title="[bold bright_white]Erro[/bold bright_white]", border_style="bold red", box=box.DOUBLE, padding=(1, 4)))

                        confirmacao.confirmacao()
                        visual.limpar_tela()

                    # Se houver votos, tenta determinar o vencedor
                    else:
                        query_verificar_vencedor = (
                            "SELECT c.nome, c.partido, c.numero_votacao, COUNT(v.id) AS total_votos "
                            "FROM candidatos c "
                            "LEFT JOIN votos v ON c.id = v.id_candidato "
                            "WHERE c.numero_votacao != '00' "
                            "GROUP BY c.id, c.nome, c.partido, c.numero_votacao "
                            "HAVING total_votos > 0 "
                            "ORDER BY total_votos DESC "
                            "LIMIT 1"
                        )
                        cursor.execute(query_verificar_vencedor)
                        vencedor = cursor.fetchone()
                        cursor.fetchall()

                        if vencedor:
                            tabela_vencedor.add_row(
                                vencedor['nome'],
                                vencedor['partido'],
                                str(vencedor['total_votos'])
                            )
                            console.print(Align.center(tabela_vencedor)) # Exibe a tabela com o vencedor
                        else:
                            console.print(Panel(Align.center("[bold yellow]Não foi possível determinar um vencedor, mesmo com votos registrados.[/bold yellow]"),
                                                title="[bold bright_white]Erro[/bold bright_white]", border_style="bold red",
                                                box=box.DOUBLE, padding=(1, 4)))
                        confirmacao.confirmacao()
                    visual.limpar_tela()
                case False:
                    executando_entrada = 0
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()