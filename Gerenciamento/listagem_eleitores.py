from database import conexao_banco as conect
from Validadores import confirmacao
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich import box
from Visual.visual import limpar_tela

console = Console(highlight=False)

def listagem_eleitores():
    """
    Recupera e exibe uma listagem consolidada de todos os eleitores do sistema.

    A função faz uma consulta completa na tabela de eleitores. Se a base estiver
    vazia, exibe uma mensagem informativa. Caso contrário, gera uma tabela centralizada
    no terminal via biblioteca Rich, convertendo as flags binárias do banco de dados
    (0 e 1) em representações textuais coloridas e amigáveis para leitura (Sim/Não e
    Já Votou/Não Votou). Ao final, exibe um contador com o total geral acumulado.

    Qualquer falha estrutural ou de comunicação com o banco é tratada internamente
    pelo bloco de exceção genérico, gerando um aviso estilizado no terminal e
    garantindo que o script feche os recursos de conexão sem travar o sistema.

    Args:
        None.

    Returns:
        None: A função tem propósito puramente de exibição gráfica de dados no console,
        não gerando retornos físicos.
    """

    limpar_tela()

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute('SELECT * FROM eleitores')
        total_eleitores = cursor.fetchall()

        if len(total_eleitores) == 0:
            console.print('\n Nenhum eleitor cadastrado no sistema.', style="bold yellow")
        else:
            tabela = Table(
                title="Listagem de Eleitores",
                box=box.DOUBLE,
                border_style="bold sandy_brown",
                title_style="bold bright_white",
                header_style="bold sandy_brown",
                show_lines=True
            ) #cria a tabela 

            tabela.add_column("ID", justify="center", style="bright_white")
            tabela.add_column("Nome", style="bright_white")
            tabela.add_column("Título de Eleitor", style="bright_white")
            tabela.add_column("Mesário", justify="center")
            tabela.add_column("Status de Votação", justify="center")

            for eleitor in total_eleitores:
                # converte 1/0 em texto colorido
                if eleitor['mesario'] == 1:
                    mesario = "[bold green]Sim[/bold green]"
                else:
                    mesario = "[dim]Não[/dim]"

                if eleitor['status_votacao'] == 1:
                    status_votacao = "[bold green]Já Votou[/bold green]"
                else:
                    status_votacao = "[dim]Não Votou[/dim]"

                tabela.add_row(
                    str(eleitor['id']),
                    eleitor['nome'],
                    eleitor['titulo_eleitor'],
                    mesario,
                    status_votacao
                )

            console.print(Align.center(tabela))
            console.print(f'\n Total de Eleitores Cadastrados: [bold white]{len(total_eleitores)}[/bold white]')

    except Exception as erro:
        console.print(f'\n Erro ao listar eleitores: {erro}', style="bold red")

    confirmacao.confirmacao()

    cursor.close()
    conexao.close()