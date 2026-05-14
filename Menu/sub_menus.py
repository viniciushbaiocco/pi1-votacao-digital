import os

if not os.environ.get('TERM'):
    os.environ['TERM'] = 'xterm-256color'

import pyfiglet  # PASSO 1: biblioteca nova que gera texto em letras grandes (ASCII art)
from rich.console import Console  # PASSO 3: Console do rich substitui print+colorama só no banner
from rich.panel import Panel      # PASSO 4: Panel cria caixas com bordas automáticas, substitui o ╔═╗ manual
from rich import box              # PASSO 4: box define o estilo da borda — usamos box.DOUBLE (╔═╗)
from rich.align import Align      # PASSO 4: Align.center() centraliza o conteúdo dentro do painel

console = Console(highlight=False)
##SOBRE O PYFIGLET:
##pyfiglet.figlet_format(texto, font="nome_fonte") devolve uma STRING com o texto desenhado em letras grandes feitas de caracteres
##usamos a fonte "big". outras fontes legais: "slant", "standard", "doom"
##pra ver todas: python3 -c "import pyfiglet; print(pyfiglet.FigletFont.getFonts())"
##a string retornada tem várias linhas basta dar print() nela e o Python já quebra as linhas certinho

subtitulo_banner = "Sistema de Votação Digital"


def exibir_banner():
    """
        Exibe o banner para estética do menu.

        Args:
            None

        Returns:
            None
        """
    # PASSO 1: gera o "LAD.PY" em letras grandes e centraliza pela largura real do terminal
    # PASSO 3: trocamos print+colorama por console.print do rich — estilo fica em style="bold cyan" etc.
    largura_terminal = os.get_terminal_size().columns
    arte_lad_py = pyfiglet.figlet_format("LAD.PY", font="standard")

    console.print("═" * largura_terminal, style="bold cyan")
    console.print()
    for linha in arte_lad_py.split('\n'):
        console.print(linha.center(largura_terminal), style="bold white")
    console.print()
    console.print(subtitulo_banner.center(largura_terminal), style="white")
    console.print()
    console.print("═" * largura_terminal, style="bold cyan")
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
        "\n"
        "  [bold yellow][1][/bold yellow]  Gerenciamento\n"
        "\n"
        "  [bold yellow][2][/bold yellow]  Votação\n"
        "\n"
        "  [bold red][3]  Finalizar Sistema[/bold red]\n"
    )

    # Align.center dentro do Panel centraliza o texto das opções dentro do painel
    console.print(Panel(Align.center(conteudo), title="[bold cyan]MENU PRINCIPAL[/bold cyan]", border_style="white", box=box.DOUBLE))


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
        "\n"
        "  [bold yellow][1][/bold yellow]  Eleitores\n"
        "  [bold yellow][2][/bold yellow]  Candidatos\n"
        "  [bold red][3]  Voltar[/bold red]\n"
    )
    console.print(Panel(Align.center(conteudo), title="[bold cyan]GERENCIAMENTO[/bold cyan]", border_style="white", box=box.DOUBLE))


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
        "\n"
        "  [bold yellow][1][/bold yellow]  Cadastrar Novos Eleitores\n"
        "  [bold yellow][2][/bold yellow]  Editar Eleitores\n"
        "  [bold yellow][3][/bold yellow]  Excluir Eleitores\n"
        "  [bold yellow][4][/bold yellow]  Buscar Eleitores\n"
        "  [bold yellow][5][/bold yellow]  Visualizar Eleitores\n"
        "  [bold red][6]  Voltar[/bold red]\n"
    )
    console.print(Panel(Align.center(conteudo), title="[bold cyan]ELEITORES[/bold cyan]", border_style="white", box=box.DOUBLE))


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
        "\n"
        "  [bold yellow][1][/bold yellow]  Cadastrar Novos Candidatos\n"
        "  [bold yellow][2][/bold yellow]  Editar Candidatos\n"
        "  [bold yellow][3][/bold yellow]  Excluir Candidatos\n"
        "  [bold yellow][4][/bold yellow]  Buscar Candidatos\n"
        "  [bold yellow][5][/bold yellow]  Visualizar Candidatos\n"
        "  [bold red][6]  Voltar[/bold red]\n"
    )
    console.print(Panel(Align.center(conteudo), title="[bold cyan]CANDIDATOS[/bold cyan]", border_style="white", box=box.DOUBLE))


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
        "\n"
        "  [bold yellow][1][/bold yellow]  Abrir Sistema De Votação\n"
        "  [bold yellow][2][/bold yellow]  Resultados Da Votação\n"
        "  [bold yellow][3][/bold yellow]  Ocorrências\n"
        "  [bold red][4]  Voltar[/bold red]\n"
    )
    console.print(Panel(Align.center(conteudo), title="[bold cyan]VOTAÇÃO[/bold cyan]", border_style="white", box=box.DOUBLE))


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
        "\n"
        "  [bold yellow][1][/bold yellow]  Votar\n"
        "  [bold yellow][2][/bold yellow]  Encerrar Sistema De Votação\n"
    )
    console.print(Panel(Align.center(conteudo), title="[bold cyan]SISTEMA DE VOTAÇÃO[/bold cyan]", border_style="white", box=box.DOUBLE))


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
        "\n"
        "  [bold yellow][1][/bold yellow]  Boletim De Urna\n"
        "  [bold yellow][2][/bold yellow]  Estatísticas De Comparecimento\n"
        "  [bold yellow][3][/bold yellow]  Votos Por Partido\n"
        "  [bold yellow][4][/bold yellow]  Validação De Integridade\n"
        "  [bold red][5]  Voltar[/bold red]\n"
    )
    console.print(Panel(Align.center(conteudo), title="[bold cyan]RESULTADOS DA VOTAÇÃO[/bold cyan]", border_style="white", box=box.DOUBLE))

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
        "\n"
        "  [bold yellow][1][/bold yellow]  Abertura de Urna\n"
        "  [bold yellow][2][/bold yellow]  Acesso Negado\n"
        "  [bold yellow][3][/bold yellow]  Encerramento de Urna\n"
        "  [bold yellow][4][/bold yellow]  Voto Computado\n"
        "  [bold yellow][5][/bold yellow]  Voto Duplo\n"
        "  [bold yellow][6][/bold yellow]  Gerais\n"
        "  [bold red][7]  Voltar[/bold red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold cyan]OCORRÊNCIAS[/bold cyan]", border_style="white", box=box.DOUBLE))