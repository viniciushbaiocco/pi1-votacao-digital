import time

from Menu import sub_menus
from database import conexao_banco
from Validadores import confirmacao, gerenciador_de_entrada
from Visual import visual
from rich.console import Console
from rich.table import Table
from rich import box, style
from rich.align import Align

console = Console(highlight=False)

def exibir_boletim_urna():
    """
    Gerencia a exibição do boletim de urna, permitindo ao usuário listar candidatos
    com seus respectivos votos ou determinar o vencedor da eleição.

    Args:
        None

    Returns:
        Listagem ou o Vencedor
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
                title="Listagem de Eleitores",
                box=box.DOUBLE,
                border_style="bold sandy_brown",
                title_style="bold bright_white",
                header_style="bold sandy_brown",
                show_lines=True
            )

            tabela.add_column("Nome", style="bright_white")
            tabela.add_column("Partido", style="bright_white")
            tabela.add_column("Total de Votos", justify="center")

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
            tabela_vencedor.add_column("Total de Votos", justify="center")

            match escolha:
                # Opção 1: Listar todos os candidatos com seus votos
                case 1:
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

                    visual.carregar_pontos_loop(3, "Listando Candidatos") # implementar cor com o rich
                    time.sleep(1)
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
                        console.print("[bold red]Nenhum Voto Registrado[/bold red]")
                        console.print("\n[bold yellow]Vencedor não pode ser definido![/bold yellow]")

                        confirmacao.confirmacao()
                        visual.limpar_tela()

                    # Se houver votos, tenta determinar o vencedor
                    else:
                        query_verificar_vencedor =  ('SELECT c.nome, c.partido, '
                                                     'COUNT(v.id) AS total_votos '
                                                     'FROM candidatos c '
                                                     'LEFT JOIN votos v '
                                                     'ON c.id = v.id_candidato '
                                                     'GROUP BY c.id, c.nome, c.partido '
                                                     ' ORDER BY total_votos DESC')
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
                        # Caso não seja possível determinar um vencedor (improvável com a query atual, mas como fallback)
                        else:
                            console.print("[bold yellow]Não foi possível determinar um vencedor, mesmo com votos registrados.[/bold yellow]")

                    # Pausa e limpa a tela após exibir o resultado (movido para fora do if/else para consistência)
                    confirmacao.confirmacao()
                    visual.limpar_tela()
                case False:
                    executando_entrada = 0
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()