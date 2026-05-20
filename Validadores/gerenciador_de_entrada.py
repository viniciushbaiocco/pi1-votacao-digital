from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich import box

console = Console(highlight=False)

def formatar_cpf_digitado(digitos):
    """
    Formata uma string de dígitos no padrão visual de CPF (XXX.XXX.XXX-XX),
    adicionando pontos e traço conforme o número de dígitos informados.

    Args:
        digitos (str): String contendo apenas os dígitos do CPF (até 11).

    Returns:
        str: CPF formatado parcialmente ou completamente, conforme o número de dígitos.
    """
    d = digitos[:11]
    if len(d) <= 3:
        return d
    elif len(d) <= 6:
        return f"{d[:3]}.{d[3:]}"
    elif len(d) <= 9:
        return f"{d[:3]}.{d[3:6]}.{d[6:]}"
    else:
        return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"


def formatar_cpf_display(cpf):
    """
    Formata um CPF de 11 dígitos crus (sem pontuação) para exibição: XXX.XXX.XXX-XX.
    Útil para exibir o CPF descriptografado em tabelas.

    Args:
        cpf (str): CPF com ou sem formatação.

    Returns:
        str: CPF no formato XXX.XXX.XXX-XX, ou o valor original se não tiver 11 dígitos.
    """
    apenas_digitos = ''.join(c for c in cpf if c.isdigit())
    if len(apenas_digitos) == 11:
        return f"{apenas_digitos[:3]}.{apenas_digitos[3:6]}.{apenas_digitos[6:9]}-{apenas_digitos[9:]}"
    return cpf


def input_cpf_mascarado(mensagem="Digite o CPF", titulo="CPF"):
    """
    Exibe um painel de entrada e captura o CPF do usuário com máscara em tempo real,
    formatando automaticamente para XXX.XXX.XXX-XX conforme os dígitos são digitados.
    Apenas dígitos são aceitos. ESC cancela a operação.

    Args:
        mensagem (str): Texto de instrução exibido dentro do painel.
        titulo (str): Título do painel de entrada.

    Returns:
        str: CPF no formato XXX.XXX.XXX-XX, ou None se o usuário cancelar.
    """
    from prompt_toolkit import prompt as prompt_toolkit_input
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.document import Document

    conteudo = f"[bright_white]{mensagem}[/bright_white]\n[dim]ESC - Cancelar[/dim]"
    console.print(Panel(Align.center(conteudo), title=f"[bold bright_white]{titulo}[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))

    teclas = KeyBindings()

    @teclas.add('<any>', eager=True)
    def capturar_digito(event):
        buffer = event.app.current_buffer
        digitos_atuais = ''.join(c for c in buffer.text if c.isdigit())
        if event.data.isdigit() and len(digitos_atuais) < 11:
            digitos_atuais += event.data
            cpf_formatado = formatar_cpf_digitado(digitos_atuais)
            buffer.set_document(Document(cpf_formatado, len(cpf_formatado)))

    @teclas.add('c-h', eager=True)
    @teclas.add('backspace', eager=True)
    def apagar_digito(event):
        buffer = event.app.current_buffer
        digitos_atuais = ''.join(c for c in buffer.text if c.isdigit())
        if digitos_atuais:
            digitos_atuais = digitos_atuais[:-1]
            cpf_formatado = formatar_cpf_digitado(digitos_atuais)
            buffer.set_document(Document(cpf_formatado, len(cpf_formatado)))

    @teclas.add('escape', eager=True)
    def cancelar(event):
        event.app.exit(result='\x00')

    try:
        cpf_digitado = prompt_toolkit_input("» ", key_bindings=teclas)
    except (KeyboardInterrupt, EOFError):
        return None

    if cpf_digitado == '\x00':
        return None

    return cpf_digitado

def input_cancelavel(prompt, titulo=""):
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
                    executando_entrada = 1
                    return escolha
                elif min_val == max_val or max_val == min_val:
                    console.print("Erro: Opção inválida. Por favor, escolha dentre as opções mostradas.", style="bold red")
                else:
                    console.print(f"Erro: Opção inválida. Por favor, escolha uma opção entre {min_val} e {max_val}.", style="bold red")
            except ValueError:
                console.print("Erro: Entrada inválida. Por favor, digite um número inteiro ou digite 'X' para retornar.", style="bold red")