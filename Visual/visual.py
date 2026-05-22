import time
import os
import sys

# Códigos ANSI para cor e estilo
BOLD_YELLOW = "\033[1;33m" # 1 para negrito, 33 para amarelo
RESET = "\033[0m"

def carregar_pontos_loop(ciclos, mensagem):
    """
    Exibe uma animação contínua de carregamento com pontos incrementais em uma CLI.

    A função simula um feedback visual de processamento assíncrono imprimindo a mensagem
    fornecida acompanhada de pontos que crescem sequencialmente (de 0 a 3 pontos).
    Para garantir uma atualização fluida na mesma linha do terminal e evitar artefatos
    visuais de rastros anteriores, ela utiliza duas diretrizes técnicas:

    Retorno de carro (`\r`): Move o cursor de escrita de volta para o início da linha.
    Sequência ANSI (`\033[K`): Limpa todos os caracteres residuais à direita do cursor.

    O `sys.stdout.flush()` é invocado explicitamente a cada iteração para forçar
    o esvaziamento do buffer de saída do sistema operacional, garantindo que o delay
    do `time.sleep` funcione de maneira síncrona com a renderização da tela.

    Args:
        ciclos (int): O quantitativo de vezes que a sequência completa de animação
        (0, 1, 2 e 3 pontos) será iterada.
        mensagem (str): O texto descritivo que precede os pontos suspensivos
        (ex: "Consultando Resultados", "Validando Integridade").

    Returns:
        None: A função manipula diretamente o buffer de saída padrão (stdout) do terminal.
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
    Limpa o buffer de exibição e redefine o topo do console corrente.

    A rotina avalia a propriedade de ambiente de subprocesso `os.name` para disparar o
    comando nativo correspondente ao núcleo da plataforma hospedeira: `cls` se o script
    estiver rodando em ambiente Windows (`nt`) ou `clear` caso resida sob sistemas
    POSIX/Unix-like (como distribuições Linux ou macOS).

    Args:
        None.

    Returns:
        None: A função delega a chamada diretamente ao shell do sistema operacional.
    """
    os.system('cls' if os.name == 'nt' else 'clear')