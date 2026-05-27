from time import sleep

from rich import box
from rich.align import Align
from rich.console import Console
from rich.table import Table

from Validadores import confirmacao, validacao_nome, validacao_candidato, validacao_partido
from Validadores import gerenciador_de_entrada as ge
from Verificadores import verificacao_candidato_banco
from Visual.visual import limpar_tela
from database import conexao_banco

console = Console(highlight=False)


def exibir_progresso(nome=None, partido=None, sigla=None, numero=None):
    """
    Exibe uma tabela estilizada no terminal com o progresso do cadastro do candidato.

    Utiliza a biblioteca Rich para renderizar uma tabela centralizada contendo
    as informações preenchidas até o momento. Caso algum campo ainda não tenha
    sido informado (seja None), ele é exibido com um caractere de interrogação.

    Args:
        nome (str, optional): Nome completo do candidato. O padrão é None.
        partido (str, optional): Nome do partido político. O padrão é None.
        sigla (str, optional): Sigla do partido político. O padrão é None.
        numero (int ou str, optional): Número de votação do candidato. O padrão é None.

    Returns:
        None: A função apenas renderiza e imprime a tabela no console, não retornando valor.
    """
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

    tabela.add_row("Nome",              f"[green]{nome}[/green]"    if nome    is not None else "[dim]─[/dim]")
    tabela.add_row("Partido",           f"[green]{partido}[/green]" if partido is not None else "[dim]─[/dim]")
    tabela.add_row("Sigla do Partido",  f"[green]{sigla}[/green]"   if sigla   is not None else "[dim]─[/dim]")
    tabela.add_row("Número de Votação", f"[green]{numero}[/green]"  if numero  is not None else "[dim]─[/dim]")

    console.print(Align.center(tabela))


def cadastrar_candidato():
    """
    Gere o fluxo passo a passo para o cadastro de um novo candidato no sistema.

    A função guia o usuário através de telas limpas e atualizadas dinamicamente
    conforme os dados (Nome, Partido, Sigla e Número) são inseridos e validados.
    Permite o cancelamento a qualquer momento através dos inputs interativos.
    Ao final, valida conflitos no banco de dados, persiste o novo registro e
    exibe um resumo do candidato cadastrado de forma estilizada.

    Args:
        None.

    Returns:
        bool ou None: Retorna True se o candidato for cadastrado com sucesso.
        Retorna None caso o usuário cancele a operação em qualquer etapa ou
        se houver alguma falha de validação/conflito com regras de negócio.
    """
    limpar_tela()

    exibir_progresso()
    nome = validacao_nome.validar_nome()
    if nome is None:
        return None

    limpar_tela()
    exibir_progresso(nome=nome)
    partido = ge.input_cancelavel("Digite o nome do Partido", "PARTIDO")
    if partido is None:
        return None

    while not validacao_partido.validacao_partido(partido):
        limpar_tela()
        exibir_progresso(nome=nome)
        partido = ge.input_cancelavel("Partido inválido. Digite novamente", "PARTIDO")
        if partido is None:
            return None
    partido = " ".join(partido.split())

    limpar_tela()
    exibir_progresso(nome=nome, partido=partido)
    sigla = ge.input_cancelavel("Digite a Sigla do Partido (2 a 6 letras)", "SIGLA DO PARTIDO")
    if sigla is None:
        return None
    sigla = sigla.replace(" ", "").upper()

    while not validacao_candidato.validacao_sigla_partido(sigla):
        limpar_tela()
        exibir_progresso(nome=nome, partido=partido)
        sigla = ge.input_cancelavel("Sigla inválida. Digite novamente", "SIGLA DO PARTIDO")
        if sigla is None:
            return None
        sigla = sigla.replace(" ", "").upper()

    limpar_tela()
    exibir_progresso(nome=nome, partido=partido, sigla=sigla)
    numero = ge.input_cancelavel("Digite o Número de Votação (2 dígitos)", "NÚMERO DE VOTAÇÃO")
    if numero is None:
        return None
    numero = numero.replace(" ", "")

    while not validacao_candidato.validacao_numero_votacao(numero):
        limpar_tela()
        exibir_progresso(nome=nome, partido=partido, sigla=sigla)
        numero = ge.input_cancelavel("Número inválido. Digite novamente", "NÚMERO DE VOTAÇÃO")
        if numero is None:
            return None
        numero = numero.replace(" ", "")

    if numero == '00':
        limpar_tela()
        console.print("\nNúmero 00 é reservado para votos nulos e não pode ser cadastrado.", style="bold red")
        sleep(1.5)
        confirmacao.confirmacao()
        return None

    if not verificacao_candidato_banco.verificar_candidato(partido, sigla, numero):
        confirmacao.confirmacao()
        return None

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
    limpar_tela()
    console.print(Align.center(tabela_final))

    cursor.close()
    conexao.close()
    confirmacao.confirmacao()
    return True
