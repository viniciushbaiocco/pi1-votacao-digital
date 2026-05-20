import os

if not os.environ.get('TERM'):
    os.environ['TERM'] = 'xterm-266color'

import pyfiglet 
from rich.console import Console
from rich.panel import Panel     
from rich import box
from rich.align import Align      # centraliza o conteúdo dentro do painel

console = Console(highlight=False)

subtitulo_banner = "Sistema de Votação Digital"


def exibir_banner():
    """
        Exibe o banner para estética do menu.

        Args:
            None

        Returns:
            None
        """
    try:
        largura_terminal = os.get_terminal_size().columns
    except OSError:
        largura_terminal = 80
    arte_lad_py = pyfiglet.figlet_format("LAD.PY", font="standard")

    cores_brasil = ["bold green", "bold green", "bold yellow", "bold yellow", "bold green", "bold green"]

    console.print("═" * largura_terminal, style="bold yellow")
    console.print()
    for i, linha in enumerate(arte_lad_py.split('\n')):
        cor = cores_brasil[i % len(cores_brasil)]
        console.print(linha.center(largura_terminal), style=cor)
    console.print()
    console.print(subtitulo_banner.center(largura_terminal), style="bright_white")
    console.print()
    console.print("═" * largura_terminal, style="bold yellow")
    console.print()

def exibir_menu_principal():
    """
    Exibe o menu principal da aplicação com as opções de gerenciamento, votação e saída.

    Args:
        None

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    exibir_banner()

    # PASSO 4: Panel substitui o ╔═╗ manual — border_style define a cor da borda
    # [[1]] usa colchetes duplos pra mostrar [1] como texto literal (rich usa [..] como tags de cor)
    conteudo = (
        "              [bold bright_white][1][/bold bright_white]  Gerenciamento\n"
        "              [bold bright_white][2][/bold bright_white]  Votação\n"
        "              [dim]──────────────────────────────[/dim]\n"
        "              [dim red][X]  Finalizar Sistema[/dim red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]MENU PRINCIPAL[/bold bright_white]", border_style="bold spring_green1", box=box.DOUBLE, padding=(1, 4)))


def exibir_menu_gerenciamento():
    """
    Exibe o menu de gerenciamento com as opções de eleitores e candidatos.

    Args:
        None

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    exibir_banner()
    conteudo = (
        "               [bold bright_white][1][/bold bright_white]  Eleitores\n"
        "               [bold bright_white][2][/bold bright_white]  Candidatos\n"
        "               [dim]──────────────────────────────[/dim]\n"
        "               [red][X]  Voltar[/red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]GERENCIAMENTO[/bold bright_white]", border_style="bold orange1", box=box.DOUBLE, padding=(1, 4)))


def exibir_menu_eleitores():
    """
    Exibe o menu de eleitores com as opções de cadastrar, editar, excluir, buscar e visualizar eleitores.

    Args:
        None

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    exibir_banner()
    conteudo = (
        "                   [bold bright_white][1][/bold bright_white]  Cadastrar Novos Eleitores\n"
        "                   [bold bright_white][2][/bold bright_white]  Editar Eleitores\n"
        "                   [bold bright_white][3][/bold bright_white]  Excluir Eleitores\n"
        "                   [bold bright_white][4][/bold bright_white]  Buscar Eleitores\n"
        "                   [bold bright_white][5][/bold bright_white]  Visualizar Eleitores\n"
        "                   [dim]──────────────────────────────[/dim]\n"
        "                   [red][X]  Voltar[/red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]ELEITORES[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))


def exibir_menu_candidatos():
    """
    Exibe o menu de candidatos com as opções de cadastrar, editar, excluir, buscar e visualizar candidatos.

    Args:
        None

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    exibir_banner()
    conteudo = (
        "                  [bold bright_white][1][/bold bright_white]  Cadastrar Novos Candidatos\n"
        "                  [bold bright_white][2][/bold bright_white]  Editar Candidatos\n"
        "                  [bold bright_white][3][/bold bright_white]  Excluir Candidatos\n"
        "                  [bold bright_white][4][/bold bright_white]  Buscar Candidatos\n"
        "                  [bold bright_white][5][/bold bright_white]  Visualizar Candidatos\n"
        "                  [dim]──────────────────────────────[/dim]\n"
        "                  [red][X]  Voltar[/red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]CANDIDATOS[/bold bright_white]", border_style="bold gold3", box=box.DOUBLE, padding=(1, 4)))


def exibir_menu_votacao():
    """
    Exibe o menu de votação com as opções de abrir o sistema de votação e resultados da votação.

    Args:
        None

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    exibir_banner()
    conteudo = (
        "                     [bold chartreuse1][1]  Abrir Sistema De Votação[/bold chartreuse1]\n"
        "                     [bold bright_white][2][/bold bright_white]  Resultados Da Votação\n"
        "                     [bold bright_white][3][/bold bright_white]  Ocorrências\n"
        "                     [dim]──────────────────────────────[/dim]\n"
        "                     [red][X]  Voltar[/red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]VOTAÇÃO[/bold bright_white]", border_style="bold dodger_blue1", box=box.DOUBLE, padding=(1, 4)))


def exibir_menu_sistema_votacao():
    """
    Exibe o menu de sistema de votação com as opções votar e encerrar o sistema de votação.

    Args:
        None

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    exibir_banner()
    conteudo = (
        "          [bold bright_white][1][/bold bright_white]  Votar\n"
        "          [bold bright_white][2][/bold bright_white]  Encerrar Sistema De Votação"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]SISTEMA DE VOTAÇÃO[/bold bright_white]", border_style="bold chartreuse1", box=box.DOUBLE, padding=(1, 4)))


def exibir_menu_restultados_votacao():
    """
    Exibe o menu de resultados da votação com as opções de boletim de urna, estatísticas de comparecimento,
    votos por partido e validação por integridade.

    Args:
        None

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    exibir_banner()
    conteudo = (
        "       [bold bright_white][1][/bold bright_white]  Boletim De Urna\n"
        "       [bold bright_white][2][/bold bright_white]  Estatísticas De Comparecimento\n"
        "       [bold bright_white][3][/bold bright_white]  Votos Por Partido\n"
        "       [bold bright_white][4][/bold bright_white]  Validação De Integridade\n"
        "       [dim]──────────────────────────────[/dim]\n"
        "       [red][X]  Voltar[/red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]RESULTADOS DA VOTAÇÃO[/bold bright_white]", border_style="bold deep_sky_blue1", box=box.DOUBLE, padding=(1, 4)))

def exibir_menu_ocorrencias():
    """
    Exibe o menu de ocorrências.

    Args:
        None

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    exibir_banner()
    conteudo = (
        "                 [bold bright_white][1][/bold bright_white]  Abertura de Urna\n"
        "                 [bold bright_white][2][/bold bright_white]  Acesso Negado\n"
        "                 [bold bright_white][3][/bold bright_white]  Encerramento de Urna\n"
        "                 [bold bright_white][4][/bold bright_white]  Voto Computado\n"
        "                 [bold bright_white][5][/bold bright_white]  Voto Duplo\n"
        "                 [bold bright_white][6][/bold bright_white]  Gerais\n"
        "                 [dim]──────────────────────────────[/dim]\n"
        "                 [red][X]  Voltar[/red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]OCORRÊNCIAS[/bold bright_white]", border_style="bold dark_orange", box=box.DOUBLE, padding=(1, 4)))

def exibir_menu_boletim_urna():
    os.system('cls' if os.name == 'nt' else 'clear')
    exibir_banner()
    conteudo = (
        "                 [bold bright_white][1][/bold bright_white]  Listagem dos Candidatos\n"
        "                 [bold bright_white][2][/bold bright_white]  Verificar Vencedor\n"
        "                 [red][X]  Voltar[/red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]OCORRÊNCIAS[/bold bright_white]", border_style="bold dark_orange", box=box.DOUBLE, padding=(1, 4)))