import os

if not os.environ.get('TERM'):
    os.environ['TERM'] = 'xterm-256color'

from colorama import Fore, Style, init

##PARA QUEM QUISER EDITAR: 
##os comandos FORE mudam cor do texto(foreground)
##os comandos STYLE mudam o estilo do texto(bright,normal,dim, reset_all(importante pq ele reseta as cores sem vazar pro proximo print))
##ESTRUTURA DE COR DO TEXTO: Fore.Cor
##ESTRUTURA DE ESTILO DO TEXTO: Style.estilo 
##Backgrounds (nao usei ainda): segue a estrutura de cor de texto: Back.Cor (mesmas cores disponiveis)
#pra vcs descobrirem as opçoes, digita a variavel Fore ou Style, e da um . (o "auto complete" mostra as opcoes)

init(autoreset=True) #cada print reseta o estilo formatado pelo anterior


largura = 36
banner = "LAD.Py | Sistema de Votação Digital"
largura_banner = len(banner) + 8


def exibir_banner():
    espacos = "    " #4 espaços
    print(Fore.GREEN + "╔" + "═" * largura_banner + "╗")
    print(Fore.GREEN + "║" + Fore.YELLOW + Style.BRIGHT + espacos + banner + espacos + Style.RESET_ALL + Fore.GREEN + "║")
    print(Fore.GREEN + "╚" + "═" * largura_banner + "╝")
    print()


def exibir_menu_principal():
    """
    Exibe o menu principal da aplicação com as opções de gerenciamento, votação e saída.

    Args:
        None

    Returns:
        None
    """
    #executa uma limpeza do terminal cada opcao executada
    os.system('cls' if os.name == 'nt' else 'clear')#cls foi usado pra nao atrapalhar minha vida e do leo, cls é do linux e clear é do windows
    exibir_banner()
    print(Fore.LIGHTWHITE_EX + "╔" + "═" * largura)
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "║" + Fore.CYAN + Style.BRIGHT + "MENU PRINCIPAL".center(largura))
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "╠" + "═" * largura)
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[1]" + Fore.WHITE + "  Gerenciamento")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[2]" + Fore.WHITE + "  Votação")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.RED + "[3]  Sair")
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "╚" + "═" * largura)


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
    print(Fore.LIGHTWHITE_EX + "╔" + "═" * largura)
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "║" + Fore.CYAN + Style.BRIGHT + "GERENCIAMENTO".center(largura))
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "╠" + "═" * largura)
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[1]" + Fore.WHITE + "  Eleitores")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[2]" + Fore.WHITE + "  Candidatos")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.RED + "[3]  Voltar")
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "╚" + "═" * largura)


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
    print(Fore.LIGHTWHITE_EX + "╔" + "═" * largura)
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "║" + Fore.CYAN + Style.BRIGHT + "ELEITORES".center(largura))
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "╠" + "═" * largura)
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[1]" + Fore.WHITE + "  Cadastrar Novos Eleitores")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[2]" + Fore.WHITE + "  Editar Eleitores")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[3]" + Fore.WHITE + "  Excluir Eleitores")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[4]" + Fore.WHITE + "  Buscar Eleitores")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[5]" + Fore.WHITE + "  Visualizar Eleitores")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.RED + "[6]  Voltar")
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "╚" + "═" * largura)


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
    print(Fore.LIGHTWHITE_EX + "╔" + "═" * largura)
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "║" + Fore.CYAN + Style.BRIGHT + "CANDIDATOS".center(largura))
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "╠" + "═" * largura)
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[1]" + Fore.WHITE + "  Cadastrar Novos Candidatos")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[2]" + Fore.WHITE + "  Editar Candidatos")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[3]" + Fore.WHITE + "  Excluir Candidatos")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[4]" + Fore.WHITE + "  Buscar Candidatos")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[5]" + Fore.WHITE + "  Visualizar Candidatos")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.RED + "[6]  Voltar")
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "╚" + "═" * largura)


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
    print(Fore.LIGHTWHITE_EX + "╔" + "═" * largura)
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "║" + Fore.CYAN + Style.BRIGHT + "VOTAÇÃO".center(largura))
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "╠" + "═" * largura)
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[1]" + Fore.WHITE + "  Abrir Sistema De Votação")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[2]" + Fore.WHITE + "  Resultados Da Votação")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.RED + "[3]  Voltar")
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "╚" + "═" * largura)


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
    print(Fore.LIGHTWHITE_EX + "╔" + "═" * largura)
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "║" + Fore.CYAN + Style.BRIGHT + "SISTEMA DE VOTAÇÃO".center(largura))
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "╠" + "═" * largura)
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[1]" + Fore.WHITE + "  Votar")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[2]" + Fore.WHITE + "  Encerrar Sistema De Votação")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.RED + "[3]  Voltar")
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "╚" + "═" * largura)


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
    print(Fore.LIGHTWHITE_EX + "╔" + "═" * largura)
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "║" + Fore.CYAN + Style.BRIGHT + "RESULTADOS DA VOTAÇÃO".center(largura))
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "╠" + "═" * largura)
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[1]" + Fore.WHITE + "  Boletim De Urna")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[2]" + Fore.WHITE + "  Estatísticas De Comparecimento")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[3]" + Fore.WHITE + "  Votos Por Partido")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.YELLOW + Style.BRIGHT + "[4]" + Fore.WHITE + "  Validação De Integridade")
    print(Fore.LIGHTWHITE_EX + "║  " + Fore.RED + "[5]  Voltar")
    print(Fore.LIGHTWHITE_EX + "║")
    print(Fore.LIGHTWHITE_EX + "╚" + "═" * largura)
