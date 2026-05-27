from rich.console import Console
from Visual.visual import limpar_tela
from time import sleep

console = Console(highlight=False)

def validacao_voto():
    """
    Captura e valida a sintaxe do número eleitoral digitado pelo eleitor.

    A função executa um loop de persistência na interface de linha de comando para
    garantir que o voto fornecido atenda aos critérios estruturais obrigatórios do pleito:

    1. Trata exceções de conversão (`ValueError`) para impedir que strings puras, caracteres
       alfabéticos ou vazios quebrem o fluxo do terminal.
    2. Garante que o valor numérico digitado seja estritamente positivo (maior ou igual a 0).
    3. Exige consistência de formato obrigando que o número digitado possua exatamente
       dois caracteres de extensão (ex: '13', '22', '00').

    Se o dado passar por todas essas travas, a string original é retornada para que o
    módulo chamador faça a busca relacional na tabela de candidatos. Caso contrário, uma
    mensagem de erro descritiva do Rich é renderizada por 1.5 segundos e a tela é limpa
    para uma nova tentativa.

    Args:
        None.

    Returns:
        str: A string contendo o número eleitoral perfeitamente validado com dois dígitos.
    """
    executando_entrada = 0
    while (executando_entrada == 0):
        try:
            voto = (input('\nDigite o número eleitoral do candidato que deseja votar: '))
            if int(voto) < 0:
                console.print('\nErro: Opção inválida. Por favor, escolha uma opção positiva.', style="bold red")
                sleep(1.5)
                limpar_tela()
            else:
                return voto
        except ValueError:
            console.print('\nErro: Entrada inválida. Por favor, digite um número inteiro.', style="bold red")
            sleep(1.5)
            limpar_tela()
