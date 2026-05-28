import os

if not os.environ.get('TERM'):
    os.environ['TERM'] = 'xterm-266color'

import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.align import Align      # centraliza o conteúdo dentro do painel
from Visual.visual import limpar_tela

VERDE = "#21A500"
AMARELO = "#FFD000"
LARANJA = "#D4620A"

console = Console(highlight=False)

subtitulo_banner = "Sistema de Votação Digital"


def exibir_banner():
    """
    Gera e exibe o banner estético em arte ASCII estilizado com as cores do Brasil.

    A função calcula dinamicamente a largura atual da janela do terminal utilizando o
    módulo `os`. Caso o script seja executado em um ambiente sem suporte (como saídas
    de logs ou pipes), adota 80 colunas como fallback. A palavra 'LAD.PY' é convertida
    em arte ASCII via PyFiglet e impressa linha a linha aplicando cores alternadas
    (verde e amarelo) de forma centralizada.

    Args:
        None.

    Returns:
        None: A função realiza apenas impressões no console.
    """
    try:
        largura_terminal = os.get_terminal_size().columns
    except OSError:
        largura_terminal = 80
    arte_lad_py = pyfiglet.figlet_format("LAD.PY", font="standard")

    cores_brasil = [f"bold {VERDE}", f"bold {VERDE}", f"bold {AMARELO}", f"bold {AMARELO}", f"bold {VERDE}", f"bold {VERDE}"]

    console.print("═" * largura_terminal, style=f"bold {AMARELO}")
    console.print()
    for i, linha in enumerate(arte_lad_py.split('\n')):
        cor = cores_brasil[i % len(cores_brasil)]
        console.print(linha.center(largura_terminal), style=cor)
    console.print()
    console.print(subtitulo_banner.center(largura_terminal), style="bright_white")
    console.print()
    console.print("═" * largura_terminal, style=f"bold {AMARELO}")
    console.print()

def exibir_menu_principal():
    """
    Renderiza a interface gráfica do Menu Principal no terminal.

    Limpa a tela do terminal de acordo com o sistema operacional ativo (Windows ou
    Unix-based), imprime o cabeçalho dinâmico e monta um painel Rich contendo as
    rotas principais da Urna: Gerenciamento e Votação.

    Args:
        None.

    Returns:
        None: A função realiza apenas impressões no console.
    """
    limpar_tela()
    exibir_banner()

    # PASSO 4: Panel substitui o ╔═╗ manual — border_style define a cor da borda
    # [[1]] usa colchetes duplos pra mostrar [1] como texto literal (rich usa [..] como tags de cor)
    conteudo = (
        "              [bold bright_white][1][/bold bright_white]  Gerenciamento\n"
        "              [bold bright_white][2][/bold bright_white]  Votação\n"
        "              [dim]──────────────────────────────[/dim]\n"
        "              [red][X]  Finalizar Sistema[/red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]MENU PRINCIPAL[/bold bright_white]", border_style=f"bold {VERDE}", box=box.DOUBLE, padding=(1, 4)))


def exibir_menu_gerenciamento():
    """
    Renderiza a interface gráfica do Menu de Gerenciamento.

    Apresenta as opções administrativas para triagem e direcionamento entre os
    módulos específicos de eleitores ou candidatos cadastrados no sistema.

    Args:
        None.

    Returns:
        None: A função realiza apenas impressões no console.
    """
    limpar_tela()
    exibir_banner()
    conteudo = (
        "               [bold bright_white][1][/bold bright_white]  Eleitores\n"
        "               [bold bright_white][2][/bold bright_white]  Candidatos\n"
        "               [dim]──────────────────────────────[/dim]\n"
        "               [red][X]  Voltar[/red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]GERENCIAMENTO[/bold bright_white]", border_style=f"bold {LARANJA}", box=box.DOUBLE, padding=(1, 4)))


def exibir_menu_eleitores():
    """
    Renderiza a interface gráfica com o Menu de Controle e Relatórios de Eleitores.

    Exibe o painel consolidado com todas as operações cadastrais (CRUD), consultas
    por CPF/Título, listagens em lote e a rotina de recuperação de chave de acesso de backup.

    Args:
        None.

    Returns:
        None: A função realiza apenas impressões no console.
    """
    limpar_tela()
    exibir_banner()
    conteudo = (
        "                   [bold bright_white][1][/bold bright_white]  Cadastrar Novos Eleitores\n"
        "                   [bold bright_white][2][/bold bright_white]  Editar Eleitores\n"
        "                   [bold bright_white][3][/bold bright_white]  Excluir Eleitores\n"
        "                   [bold bright_white][4][/bold bright_white]  Buscar Eleitores\n"
        "                   [bold bright_white][5][/bold bright_white]  Visualizar Eleitores\n"
        "                   [bold bright_white][6][/bold bright_white]  Recuperar Chave de Acesso\n"
        "                   [dim]──────────────────────────────[/dim]\n"
        "                   [red][X]  Voltar[/red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]ELEITORES[/bold bright_white]", border_style=f"bold {LARANJA}", box=box.DOUBLE, padding=(1, 4)))


def exibir_menu_candidatos():
    """
    Renderiza a interface gráfica com o Menu de Controle e Relatórios de Candidatos.

    Exibe o painel consolidado contendo as opções de inclusão, alteração, remoção por número
    de urna, busca exata/parcial e listagem geral de partidos e candidatos.

    Args:
        None.

    Returns:
        None: A função realiza apenas impressões no console.
    """
    limpar_tela()
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
    Renderiza a interface gráfica do Menu Operacional de Votação.

    Disponibiliza os caminhos críticos para abertura do sistema interativo de votação,
    módulo de apuração/estatísticas e acesso aos relatórios e logs de ocorrência emitidos.

    Args:
        None.

    Returns:
        None: A função realiza apenas impressões no console.
    """
    limpar_tela()
    exibir_banner()
    conteudo = (
        f"                     [bold {VERDE}][1]  Abrir Sistema De Votação[/bold {VERDE}]\n"
        "                     [bold bright_white][2][/bold bright_white]  Resultados Da Votação\n"
        "                     [bold bright_white][3][/bold bright_white]  Ocorrências\n"
        "                     [dim]──────────────────────────────[/dim]\n"
        "                     [red][X]  Voltar[/red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]VOTAÇÃO[/bold bright_white]", border_style="bold dodger_blue1", box=box.DOUBLE, padding=(1, 4)))


def exibir_menu_sistema_votacao():
    """
    Renderiza a interface gráfica do Terminal de Votação (Urna Eleitoral Ativa).

    Exibe o menu simplificado exposto ao mesário e eleitor para iniciar o fluxo de
    computação de votos individuais ou comandar o encerramento da sessão atual da seção.

    Args:
        None.

    Returns:
        None: A função realiza apenas impressões no console.
    """
    limpar_tela()
    exibir_banner()
    conteudo = (
        "          [bold bright_white][1][/bold bright_white]  Votar\n"
        "          [bold bright_white][2][/bold bright_white]  Encerrar Sistema De Votação"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]SISTEMA DE VOTAÇÃO[/bold bright_white]", border_style=f"bold {VERDE}", box=box.DOUBLE, padding=(1, 4)))


def exibir_menu_resultados_votacao():
    """
    Renderiza a interface gráfica do Menu de Relatórios de Fechamento e Auditoria.

    Apresenta caminhos para extração de dados consolidados pós-pleito, incluindo a emissão
    de Boletim de Urna, taxas de abstenção/comparecimento, votos por legenda e rotinas de
    verificação de integridade de hashes de segurança.

    Args:
        None.

    Returns:
        None: A função realiza apenas impressões no console.
    """
    limpar_tela()
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
    Renderiza a interface gráfica do Menu de Auditoria de Logs de Ocorrências.

    Exibe o catálogo com os filtros de monitoramento e rastreabilidade da urna, permitindo
    revisar logs de inicialização, tentativas de fraudes/acessos negados, logs de votos
    computados e relatórios de sessões gerais.

    Args:
        None.

    Returns:
        None: A função realiza apenas impressões no console.
    """
    limpar_tela()
    exibir_banner()
    conteudo = (
        "                 [bold bright_white][1][/bold bright_white]  Abertura de Urna\n"
        "                 [bold bright_white][2][/bold bright_white]  Acesso Negado\n"
        "                 [bold bright_white][3][/bold bright_white]  Encerramento de Urna\n"
        "                 [bold bright_white][4][/bold bright_white]  Voto Computado\n"
        "                 [bold bright_white][5][/bold bright_white]  Voto Duplo\n"
        "                 [bold bright_white][6][/bold bright_white]  Protocolo de Votação\n"
        "                 [bold bright_white][7][/bold bright_white]  Gerais\n"
        "                 [dim]──────────────────────────────[/dim]\n"
        "                 [red][X]  Voltar[/red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]OCORRÊNCIAS[/bold bright_white]", border_style="bold dark_orange", box=box.DOUBLE, padding=(1, 4)))

def exibir_menu_boletim_urna():
    """
    Renderiza a interface gráfica do Menu de Detalhamento do Boletim de Urna (BU).

    Ajustei o metadado do título do painel para 'BOLETIM DE URNA' para corresponder
    corretamente ao escopo das opções expostas (Listagem de Candidatos / Verificar Vencedor).

    Args:
        None.

    Returns:
        None: A função realiza apenas impressões no console.
    """
    limpar_tela()
    exibir_banner()
    conteudo = (
        "                 [bold bright_white][1][/bold bright_white]  Listagem dos Candidatos\n"
        "                 [bold bright_white][2][/bold bright_white]  Verificar Vencedor\n"
        "                 [red][X]  Voltar[/red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]BOLETIM DE URNA[/bold bright_white]", border_style="bold dark_orange", box=box.DOUBLE, padding=(1, 4)))