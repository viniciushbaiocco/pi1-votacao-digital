from colorama import Fore, Style, init

init(autoreset=True)

def obter_entrada_inteira_valida(mensagem, min_val, max_val):
    """
    Solicita uma entrada inteira ao usuário e valida se está dentro de um intervalo.
    Continua pedindo até que uma entrada válida seja fornecida.

    Args:
        mensagem(str): A mensagem que deve ser inserida após a apresentação do menu.
        min_val(int): Valor mínimo para determinada escolha do menu.
        max_val(int): Valor máximo para determinada escolha do menu.

    Returns:
        int: Retorna o valor inteiro (opção) escolhida pelo usuário.

    """
    executando_entrada = 0
    while (executando_entrada == 0):
        try:
            escolha = int(input(Fore.WHITE + Style.BRIGHT + "\n"+mensagem))
            if min_val <= escolha <= max_val:
                executando_entrada = 1
                return escolha
            else:
                print(f"{Fore.RED}{Style.BRIGHT}Erro: Opção inválida. Por favor, escolha uma opção entre {min_val} e {max_val}.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}{Style.BRIGHT}Erro: Entrada inválida. Por favor, digite um número inteiro.{Style.RESET_ALL}")