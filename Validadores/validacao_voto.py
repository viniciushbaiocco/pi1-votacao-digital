from colorama import Fore,Style
from Visual.visual import limpar_tela
from time import sleep

def validacao_voto():
    '''
        Verifica se o voto tem dois digitos e é positivo

        Args: NONE

        Returns: Voto já verificado

    '''
    executando_entrada = 0
    while (executando_entrada == 0):
        try:
            voto = (input(Fore.WHITE + Style.BRIGHT + '\n Digite o número eleitoral do candidato que deseja votar: '))
            if int(voto) < 0:
                print(f'{Fore.RED}{Style.BRIGHT}Erro: Opção inválida. Por favor, escolha uma opção positiva. {Style.RESET_ALL}')
                sleep(1.5)
                limpar_tela()
            elif len(voto) != 2:
                print(f'{Fore.RED}{Style.BRIGHT}Erro: Opção Inválida. O número eleitoral deve conter dois digitos. {Style.RESET_ALL}')
                sleep(1.5)
                limpar_tela()
            else:
                executando_entrada = 1
                return voto
        except ValueError:
            print(f'{Fore.RED}{Style.BRIGHT}Erro: Entrada inválida. Por favor, digite um número inteiro.{Style.RESET_ALL}')
            sleep(1.5)
            limpar_tela()
