from database import conexao_banco as conect
from Validadores import confirmacao, gerenciador_de_entrada as ge, validacao_cpf as val_cpf, validacao_titulo as val_tit, validacao_palavra_chave as val_palavra
from criptografia import criptografia as cripto
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich import box
from Visual.visual import limpar_tela
from time import sleep

console = Console(highlight=False)


def recuperar_chave():
    limpar_tela()

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    cpf = ge.input_cancelavel("Digite seu CPF", "RECUPERAÇÃO DE CHAVE DE ACESSO")
    if cpf is None:
        cursor.close()
        conexao.close()
        return

    while not val_cpf.validacao_de_cpf(cpf):
        cpf = ge.input_cancelavel("CPF inválido. Digite novamente", "RECUPERAÇÃO DE CHAVE DE ACESSO")
        if cpf is None:
            cursor.close()
            conexao.close()
            return

    titulo = ge.input_cancelavel("Digite seu Título de Eleitor", "RECUPERAÇÃO DE CHAVE DE ACESSO")
    if titulo is None:
        cursor.close()
        conexao.close()
        return
    titulo = titulo.strip()

    while not val_tit.validar_titulo(titulo):
        titulo = ge.input_cancelavel("Título inválido. Digite novamente", "RECUPERAÇÃO DE CHAVE DE ACESSO")
        if titulo is None:
            cursor.close()
            conexao.close()
            return
        titulo = titulo.strip()

    cpf_criptografado = cripto.criptografar_cpf(cpf)
    cursor.execute(
        "SELECT chave_acesso, palavra_chave FROM eleitores WHERE cpf = %s AND titulo_eleitor = %s",
        (cpf_criptografado, titulo)
    )
    eleitor = cursor.fetchone()
    cursor.close()
    conexao.close()

    if eleitor is None:
        console.print(Panel(
            Align.center("[bold red]Eleitor não encontrado.[/bold red]\n[bold yellow]Verifique o CPF e Título informados.[/bold yellow]"),
            title="[bold bright_white]RECUPERAÇÃO DE CHAVE[/bold bright_white]",
            border_style="bold red",
            box=box.DOUBLE,
            padding=(1, 4)
        ))
        confirmacao.confirmacao()
        return

    if eleitor['palavra_chave'] is None:
        console.print(Panel(
            Align.center("[bold yellow]Este eleitor não possui palavra-chave de backup cadastrada.[/bold yellow]"),
            title="[bold bright_white]RECUPERAÇÃO DE CHAVE[/bold bright_white]",
            border_style="bold yellow",
            box=box.DOUBLE,
            padding=(1, 4)
        ))
        confirmacao.confirmacao()
        return

    palavra = ge.input_cancelavel("Digite sua palavra-chave de backup", "PALAVRA-CHAVE DE BACKUP")
    if palavra is None:
        return
    palavra = palavra.upper()

    while not val_palavra.validacao_palavra_chave(palavra):
        palavra = ge.input_cancelavel("Palavra inválida. Digite novamente", "PALAVRA-CHAVE DE BACKUP")
        if palavra is None:
            return
        palavra = palavra.upper()

    palavra_criptografada = cripto.criptografar_palavra_chave(palavra)

    if palavra_criptografada != eleitor['palavra_chave']:
        console.print(Panel(
            Align.center("[bold red]Palavra-chave incorreta. Acesso negado.[/bold red]"),
            title="[bold bright_white]RECUPERAÇÃO DE CHAVE[/bold bright_white]",
            border_style="bold red",
            box=box.DOUBLE,
            padding=(1, 4)
        ))
        confirmacao.confirmacao()
        return

    chave_original = cripto.descriptografar_chave_acesso(eleitor['chave_acesso'])
    console.print(Panel(
        Align.center(f"[bold green]Chave de acesso recuperada com sucesso![/bold green]\n\n[bold yellow]{chave_original}[/bold yellow]"),
        title="[bold bright_white]RECUPERAÇÃO DE CHAVE[/bold bright_white]",
        border_style="bold green",
        box=box.DOUBLE,
        padding=(1, 4)
    ))
    confirmacao.confirmacao()
