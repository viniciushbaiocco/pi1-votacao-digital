from colorama import Fore,Style

def validacao_voto():
    executando_entrada = 0
    while (executando_entrada == 0):
        try:
            voto = int(input(Fore.WHITE + Style.BRIGHT + '\n Digite o número eleitoral do candidato que deseja votar: '))
            if voto <0:
                print(f'{Fore.RED}{Style.BRIGHT}Erro: Opção inválida. Por favor, escolha uma opção positiva. {Style.RESET_ALL}')
            else:
                executando_entrada = 1
                return voto
        except ValueError:
            print(f'{Fore.RED}{Style.BRIGHT}Erro: Entrada inválida. Por favor, digite um número inteiro.{Style.RESET_ALL}')