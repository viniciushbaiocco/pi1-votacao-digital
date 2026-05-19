from rich.console import Console
from Visual.visual import limpar_tela
from time import sleep

console = Console(highlight=False)

def validacao_voto():
    '''
        Verifica se o voto tem dois digitos e é positivo

        Args: NONE

        Returns: Voto já verificado

    '''
    executando_entrada = 0
    while (executando_entrada == 0):
        try:
            voto = (input('\n Digite o número eleitoral do candidato que deseja votar: '))
            if int(voto) < 0:
                console.print('Erro: Opção inválida. Por favor, escolha uma opção positiva.', style="bold red")
                sleep(1.5)
                limpar_tela()
            elif len(voto) != 2:
                console.print('Erro: Opção Inválida. O número eleitoral deve conter dois digitos.', style="bold red")
                sleep(1.5)
                limpar_tela()
            else:
                executando_entrada = 1
                return voto
        except ValueError:
            console.print('Erro: Entrada inválida. Por favor, digite um número inteiro.', style="bold red")
            sleep(1.5)
            limpar_tela()
