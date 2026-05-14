# main.py
import os
from Menu import menu_completo
from colorama import init, Fore, Style
import pyfiglet  # PASSO 2: mesmo pyfiglet do banner, usado aqui na splash screen
from rich.console import Console

# PASSO 2: splash screen exibida UMA VEZ só na inicialização do sistema
def exibir_splash():
    os.system('cls' if os.name == 'nt' else 'clear')

    largura_terminal = os.get_terminal_size().columns

    arte = pyfiglet.figlet_format("LAD.PY", font="big")

    print(Fore.CYAN + Style.BRIGHT + ("═" * largura_terminal))
    print()
    for linha in arte.split('\n'):
        print(Fore.WHITE + Style.BRIGHT + linha.center(largura_terminal))
    print(Fore.WHITE + Style.BRIGHT +"Sistema de Votacao Digital".center(largura_terminal))
    print()
    print(Fore.CYAN + Style.BRIGHT + ("═" * largura_terminal))
    print()
    print(Fore.WHITE + "Sistema eleitoral digital.".center(largura_terminal))
    print(Fore.WHITE +"Sistema arquitetado sob pilares de segurança de ponta a ponta, garantindo integridade da votação.".center(largura_terminal))
    print()
    print(Fore.CYAN + Style.BRIGHT + ("═" * largura_terminal))
    print()
    input(Fore.WHITE + "Pressione Enter para iniciar...".center(largura_terminal))

if __name__ == "__main__":
    init(autoreset=True)
    exibir_splash()
    menu_completo.menu_completo()
