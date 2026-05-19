from Validadores import gerenciador_de_entrada as ge, validacao_titulo as val_tit
from Validadores import validacao_cpf_votacao as val_cpf_vot
from Validadores import validacao_chave_acesso as val_chave
from Validadores import confirmacao
from Verificadores import verificacao_mesario_banco as ver_mes
from Ocorrencias import acesso_negado, geral
from criptografia import criptografia as crip
from Visual.visual import limpar_tela
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich import box

console = Console(highlight=False)

def exibir_progresso_mesario(titulo=None, cpf_4=None, chave=None):
    tabela = Table(
        title="Identificação do Mesário",
        box=box.DOUBLE,
        border_style="bold chartreuse1",
        title_style="bold bright_white",
        header_style="bold chartreuse1",
        show_lines=True
    )
    tabela.add_column("Campo", style="bright_white", min_width=22)
    tabela.add_column("Valor", min_width=30)

    tabela.add_row("Título de Eleitor", f"[dim green]{titulo}[/dim green]" if titulo is not None else "[dim]─[/dim]")
    tabela.add_row("CPF (4 primeiros dígitos)", f"[dim green]{cpf_4}[/dim green]" if cpf_4 is not None else "[dim]─[/dim]")
    tabela.add_row("Chave de Acesso", f"[dim green]Confirmada[/dim green]" if chave is not None else "[dim]─[/dim]")

    console.print(Align.center(tabela))

def autenticar_mesario(id_sessao):
    limpar_tela()

    exibir_progresso_mesario()
    titulo = ge.input_cancelavel("Digite seu Título de Eleitor", "IDENTIFICAÇÃO DO MESÁRIO")
    if titulo is None:
        return False

    titulo_valido = val_tit.validar_titulo(titulo)
    while titulo_valido == False:
        limpar_tela()
        exibir_progresso_mesario()
        titulo = ge.input_cancelavel("Título inválido. Digite novamente", "IDENTIFICAÇÃO DO MESÁRIO")
        if titulo is None:
            break
        titulo_valido = val_tit.validar_titulo(titulo)
    if titulo is None:
        return False

    limpar_tela()
    exibir_progresso_mesario(titulo=titulo)
    cpf_4 = ge.input_cancelavel("Digite os 4 primeiros dígitos do seu CPF", "IDENTIFICAÇÃO DO MESÁRIO")
    if cpf_4 is None:
        return False

    cpf_4_valido = val_cpf_vot.validar_cpf_voto(cpf_4)
    while cpf_4_valido == False:
        limpar_tela()
        exibir_progresso_mesario(titulo=titulo)
        cpf_4 = ge.input_cancelavel("CPF inválido. Digite novamente", "IDENTIFICAÇÃO DO MESÁRIO")
        if cpf_4 is None:
            break
        cpf_4_valido = val_cpf_vot.validar_cpf_voto(cpf_4)
    if cpf_4 is None:
        return False

    limpar_tela()
    exibir_progresso_mesario(titulo=titulo, cpf_4=cpf_4)
    chave_acesso = ge.input_cancelavel("Digite sua Chave de Acesso", "IDENTIFICAÇÃO DO MESÁRIO")
    if chave_acesso is None:
        return False
    chave_acesso = chave_acesso.upper()

    chave_valida = val_chave.validar_chave_acesso(chave_acesso)
    while chave_valida == False:
        limpar_tela()
        exibir_progresso_mesario(titulo=titulo, cpf_4=cpf_4)
        chave_acesso = ge.input_cancelavel("Chave inválida. Digite novamente", "IDENTIFICAÇÃO DO MESÁRIO")
        if chave_acesso is None:
            break
        chave_acesso = chave_acesso.upper()
        chave_valida = val_chave.validar_chave_acesso(chave_acesso)
    if chave_acesso is None:
        return False

    limpar_tela()
    exibir_progresso_mesario(titulo=titulo, cpf_4=cpf_4, chave=chave_acesso)

    cpf_4_criptografado= crip.criptografar_cpf(cpf_4)
    chave_acesso_criptografada= crip.criptografar_chave_acesso(chave_acesso)

    resultado = ver_mes.verificar_mesario(titulo, cpf_4_criptografado, chave_acesso_criptografada)

    if resultado == (1,):
        console.print("\n[bold green]Mesário validado com sucesso![/bold green]")
        input("\nPressione Enter para continuar...")
        return True
    else:
        console.print("\n[bold red]Dados inválidos. Acesso negado.[/bold red]")
        confirmacao.confirmacao()
        geral.ocorrencia_acesso_negado(id_sessao)
        acesso_negado.ocorrencia_acesso_negado(id_sessao)
        return False
