from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich import box

console = Console(highlight=False)

def input_cancelavel(prompt, titulo=""):
    """
    Exibe um painel de captura de dados que permite o cancelamento voluntário do fluxo.

    A função atua como um invólucro (wrapper) seguro para a entrada do
    Python. Ela renderiza um painel Rich estilizado contendo as instruções do prompt e
    uma indicação explícita de que a tecla 'X' aborta a operação corrente.

    Caso o usuário digite 'X' (independente de espaços residuais ou uso de caixa alta/baixa),
    a rotina intercepta a ação e retorna `None`. Caso contrário, devolve a string bruta
    informada para ser tratada pelas funções chamadoras.

    Args:
        prompt (str): A instrução ou pergunta descritiva que orienta o preenchimento do
            campo (ex: "Digite seu Título de Eleitor").
        titulo (str, optional): O texto de cabeçalho exibido na borda superior do painel
            Rich. Padrão é uma string vazia.

    Returns:
        str ou None: Retorna a string contendo o valor digitado pelo usuário caso a
        operação prossiga; retorna `None` se o usuário optar por cancelar a ação digitando 'X'.
    """
    conteudo = f"[bright_white]{prompt}[/bright_white]\n[dim]X - Cancelar[/dim]"
    console.print(Panel(Align.center(conteudo), title=f"[bold bright_white]{titulo}[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))
    valor = input("» ")
    if valor.strip().upper() == "X":
        return None
    return valor

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
    while executando_entrada == 0:
        entrada_str = input("\n" + mensagem)

        if entrada_str.upper() == "X":
            return False
        else:
            try:
                escolha = int(entrada_str)
                if min_val <= escolha <= max_val:
                    return escolha
                elif min_val == max_val:
                    console.print("Erro: Opção inválida. Por favor, escolha dentre as opções mostradas.", style="bold red")
                else:
                    console.print(f"Erro: Opção inválida. Por favor, escolha uma opção entre {min_val} e {max_val}.", style="bold red")
            except ValueError:
                console.print("Erro: Entrada inválida. Por favor, digite um número inteiro ou digite 'X' para retornar.", style="bold red")
