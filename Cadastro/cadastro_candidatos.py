from Verificadores import verificacao_candidato_banco
from Validadores import confirmacao, validacao_nome, validacao_candidato, validacao_partido
from database import conexao_banco
from Visual.visual import limpar_tela
from Validadores import gerenciador_de_entrada as ge
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box
from time import sleep

console = Console(highlight=False)


def exibir_progresso(nome=None, partido=None, sigla=None, numero=None):
    tabela = Table(
        title="Cadastro de Candidato",
        box=box.DOUBLE,
        border_style="bold sandy_brown",
        title_style="bold bright_white",
        header_style="bold sandy_brown",
        show_lines=True
    )
    tabela.add_column("Campo", style="bright_white", min_width=20)
    tabela.add_column("Valor", min_width=30)

    tabela.add_row("Nome",              f"[dim green]{nome}[/dim green]"    if nome    is not None else "[dim]─[/dim]")
    tabela.add_row("Partido",           f"[dim green]{partido}[/dim green]" if partido is not None else "[dim]─[/dim]")
    tabela.add_row("Sigla do Partido",  f"[dim green]{sigla}[/dim green]"   if sigla   is not None else "[dim]─[/dim]")
    tabela.add_row("Número de Votação", f"[dim green]{numero}[/dim green]"  if numero  is not None else "[dim]─[/dim]")

    console.print(Align.center(tabela))


def cadastrar_candidato():
    limpar_tela()

    exibir_progresso()
    nome = validacao_nome.validar_nome()
    if nome is None:
        return

    limpar_tela()
    exibir_progresso(nome=nome)
    partido = ge.input_cancelavel("Digite o nome do Partido", "PARTIDO")
    if partido is None:
        return

    while not validacao_partido.validacao_partido(partido):
        limpar_tela()
        exibir_progresso(nome=nome)
        partido = ge.input_cancelavel("Partido inválido. Digite novamente", "PARTIDO")
        if partido is None:
            return

    limpar_tela()
    exibir_progresso(nome=nome, partido=partido)
    sigla = ge.input_cancelavel("Digite a Sigla do Partido (2 a 6 letras)", "SIGLA DO PARTIDO")
    if sigla is None:
        return
    sigla = sigla.upper()

    while not validacao_candidato.validacao_sigla_partido(sigla):
        limpar_tela()
        exibir_progresso(nome=nome, partido=partido)
        sigla = ge.input_cancelavel("Sigla inválida. Digite novamente", "SIGLA DO PARTIDO")
        if sigla is None:
            return
        sigla = sigla.upper()

    limpar_tela()
    exibir_progresso(nome=nome, partido=partido, sigla=sigla)
    numero = ge.input_cancelavel("Digite o Número de Votação (2 dígitos)", "NÚMERO DE VOTAÇÃO")
    if numero is None:
        return

    while not validacao_candidato.validacao_numero_votacao(numero):
        limpar_tela()
        exibir_progresso(nome=nome, partido=partido, sigla=sigla)
        numero = ge.input_cancelavel("Número inválido. Digite novamente", "NÚMERO DE VOTAÇÃO")
        if numero is None:
            return

    if not verificacao_candidato_banco.verificar_candidato(partido, sigla, numero):
        confirmacao.confirmacao()
        return

    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "INSERT INTO candidatos (nome, partido, sigla_partido, numero_votacao) VALUES (%s, %s, %s, %s)",
        (nome, partido, sigla, numero)
    )
    conexao.commit()

    cursor.execute("SELECT * FROM candidatos WHERE numero_votacao = %s", (numero,))
    candidato = cursor.fetchone()

    limpar_tela()
    exibir_progresso(nome=nome, partido=partido, sigla=sigla, numero=numero)

    tabela_final = Table(
        title="Candidato Cadastrado com Sucesso",
        box=box.DOUBLE,
        border_style="bold green",
        title_style="bold bright_white",
        header_style="bold green",
        show_lines=True
    )
    tabela_final.add_column("ID",               justify="center", style="bright_white")
    tabela_final.add_column("Nome",              style="bright_white")
    tabela_final.add_column("Partido",           style="bright_white")
    tabela_final.add_column("Sigla",             justify="center", style="bright_white")
    tabela_final.add_column("Número de Votação", justify="center", style="bright_white")

    tabela_final.add_row(
        str(candidato['id']),
        candidato['nome'],
        candidato['partido'],
        candidato['sigla_partido'],
        candidato['numero_votacao']
    )
    console.print(Align.center(tabela_final))

    cursor.close()
    conexao.close()
    confirmacao.confirmacao()
    return True
