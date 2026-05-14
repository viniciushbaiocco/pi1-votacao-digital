import time
import os
import sys

# Códigos ANSI para cor e estilo
BOLD_YELLOW = "\033[1;33m" # 1 para negrito, 33 para amarelo
RESET = "\033[0m"

def carregar_pontos_loop(ciclos, mensagem):
    """
    Exibe uma animação de carregamento com pontos em loop no terminal.

    Args:
        ciclos (int): O número de vezes que a sequência completa de pontos
                      (0 a 3 pontos) será repetida.
        mensagem (str): A string de texto a ser exibida antes dos pontos
                        (ex: "Carregando", "Processando").

    Returns:
        None
    """
    for _ in range(ciclos):
        for pontos in range(4):
            # \r move o cursor para o início da linha
            # \033[K limpa o resto da linha antiga para evitar rastros
            # Adiciona cor amarela e negrito, e reseta depois da mensagem
            print(f"\r{BOLD_YELLOW}{mensagem}{'.' * pontos}{RESET}\033[K", end="")
            sys.stdout.flush() # Força a atualização no terminal
            time.sleep(0.5) # Pausa por 0.5 segundos
            limpar_tela()

def limpar_tela():
    """
    Limpa a tela do terminal.

    Args:
        None
    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')