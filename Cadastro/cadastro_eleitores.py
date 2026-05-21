from Verificadores import verificacao_cpf_banco
from Verificadores import verificacao_titulo_banco
from Validadores import confirmacao, validacao_cpf, validacao_nome, validacao_titulo, validacao_palavra_chave
from database import conexao_banco
from criptografia import criptografia as cripto
from Cadastro import chave_acesso
from Visual.visual import limpar_tela
from Validadores import gerenciador_de_entrada as ge
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box

console = Console(highlight=False)

def exibir_progresso(cpf=None, nome=None, titulo=None, mesario=None, palavra_chave=None):
    tabela = Table(
        title="Cadastro de Eleitor",
        box=box.DOUBLE,
        border_style="bold sandy_brown",
        title_style="bold bright_white",
        header_style="bold sandy_brown",
        show_lines=True
    )
    tabela.add_column("Campo", style="bright_white", min_width=20)
    tabela.add_column("Valor", min_width=30)

    tabela.add_row("CPF",               f"[dim green]{cpf}[/dim green]"    if cpf    is not None else "[dim]─[/dim]")
    tabela.add_row("Nome",              f"[dim green]{nome}[/dim green]"   if nome   is not None else "[dim]─[/dim]")
    tabela.add_row("Título de Eleitor", f"[dim green]{titulo}[/dim green]" if titulo is not None else "[dim]─[/dim]")

    if mesario is None:
        tabela.add_row("Mesário", "[dim]─[/dim]")
    elif mesario:
        tabela.add_row("Mesário", "[dim green]Sim[/dim green]")
    else:
        tabela.add_row("Mesário", "[dim red]Não[/dim red]")

    if palavra_chave is None:
        tabela.add_row("Palavra-chave de Backup", "[dim]─[/dim]")
    elif palavra_chave is not None:
        tabela.add_row("Palavra-chave de Backup", "[dim green]Cadastrada[/dim green]")
    else:
        tabela.add_row("Palavra-chave de Backup", "[dim]Não cadastrada[/dim]")

    console.print(Align.center(tabela))

def cadastrar_eleitor():
    limpar_tela()

    exibir_progresso()
    cpf = ge.input_cancelavel("Digite o CPF do eleitor", "CPF")
    if cpf is None:
        return

    cpf_valido = validacao_cpf.validacao_de_cpf(cpf)
    while cpf_valido == False:
        limpar_tela()
        exibir_progresso()
        cpf = ge.input_cancelavel("CPF inválido. Digite novamente", "CPF")
        if cpf is None:
            break
        cpf_valido = validacao_cpf.validacao_de_cpf(cpf)
    if cpf is None:
        return

    cpf_criptografado = cripto.criptografar_cpf(cpf)
    cpf_no_banco = verificacao_cpf_banco.verificar_cpf_banco(cpf_criptografado)
    if cpf_no_banco[0] == 1:
        console.print("\n*** Eleitor já cadastrado! *** Consulte pelo Menu Gerenciamento.", style="bold yellow")
        confirmacao.confirmacao()
        return True

    limpar_tela()
    exibir_progresso(cpf=cpf)
    nome = validacao_nome.validar_nome()

    limpar_tela()
    exibir_progresso(cpf=cpf, nome=nome)
    titulo = ge.input_cancelavel("Digite o Título de Eleitor", "TÍTULO DE ELEITOR")
    if titulo is None:
        return
    titulo = ''.join(filter(str.isdigit, titulo))

    titulo_valido = validacao_titulo.validar_titulo(titulo)
    titulo_no_banco = verificacao_titulo_banco.verificar_titulo_de_eleitor_banco(titulo)
    while titulo_valido == False or titulo_no_banco == (1,):
        limpar_tela()
        exibir_progresso(cpf=cpf, nome=nome)
        titulo = ge.input_cancelavel("Título inválido ou já cadastrado. Digite novamente", "TÍTULO DE ELEITOR")
        if titulo is None:
            break
        titulo = ''.join(filter(str.isdigit, titulo))
        titulo_valido = validacao_titulo.validar_titulo(titulo)
        titulo_no_banco = verificacao_titulo_banco.verificar_titulo_de_eleitor_banco(titulo)
    if titulo is None:
        return

    limpar_tela()
    exibir_progresso(cpf=cpf, nome=nome, titulo=titulo)
    conteudo_mesario = (
        "[bold bright_white][1][/bold bright_white]  Sim\n"
        "[dim]──────────────────────────────[/dim]\n"
        "[dim][X]  Não[/dim]"
    )
    console.print(Panel(Align.center(conteudo_mesario), title="[bold bright_white]MESÁRIO[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))
    resposta = ge.obter_entrada_inteira_valida("Escolha: ", 1, 1)
    mesario = resposta == 1

    chave_acesso_original = chave_acesso.geracao_chave_acesso(nome)
    chave_criptografada   = cripto.criptografar_chave_acesso(chave_acesso_original)

    limpar_tela()
    exibir_progresso(cpf=cpf, nome=nome, titulo=titulo, mesario=mesario)
    conteudo_backup = (
        "[bold bright_white][1][/bold bright_white]  Sim\n"
        "[dim]──────────────────────────────[/dim]\n"
        "[dim][X]  Não[/dim]"
    )
    console.print(Panel(Align.center(conteudo_backup), title="[bold bright_white]CADASTRAR PALAVRA-CHAVE DE BACKUP?[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))
    opcao_backup = ge.obter_entrada_inteira_valida("Escolha: ", 1, 1)

    palavra_chave_criptografada = None
    if opcao_backup == 1:
        limpar_tela()
        exibir_progresso(cpf=cpf, nome=nome, titulo=titulo, mesario=mesario)
        palavra = ge.input_cancelavel("Digite uma palavra-chave (4 letras, sem acento)", "PALAVRA-CHAVE DE BACKUP")
        if palavra is not None:
            palavra = palavra.upper()
            while not validacao_palavra_chave.validacao_palavra_chave(palavra):
                limpar_tela()
                exibir_progresso(cpf=cpf, nome=nome, titulo=titulo, mesario=mesario)
                palavra = ge.input_cancelavel("Palavra inválida. Digite novamente", "PALAVRA-CHAVE DE BACKUP")
                if palavra is None:
                    break
                palavra = palavra.upper()
            if palavra is not None:
                palavra_chave_criptografada = cripto.criptografar_palavra_chave(palavra)

    conexao = conexao_banco.conexao_banco()
    cursor  = conexao.cursor(dictionary=True)

    cursor.execute(
        "INSERT INTO eleitores (nome, titulo_eleitor, cpf, mesario, chave_acesso, palavra_chave, status_votacao) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (nome, titulo, cpf_criptografado, mesario, chave_criptografada, palavra_chave_criptografada, False)
    )
    conexao.commit()

    cursor.execute("SELECT * FROM eleitores WHERE cpf = %s", (cpf_criptografado,))
    eleitor = cursor.fetchone()

    tem_backup = palavra_chave_criptografada is not None
    limpar_tela()
    exibir_progresso(cpf=cpf, nome=nome, titulo=titulo, mesario=mesario, palavra_chave=tem_backup)

    tabela_final = Table(
        title="Eleitor Cadastrado com Sucesso",
        box=box.DOUBLE,
        border_style="bold green",
        title_style="bold bright_white",
        header_style="bold green",
        show_lines=True
    )
    tabela_final.add_column("ID",                justify="center", style="bright_white")
    tabela_final.add_column("Nome",              style="bright_white")
    tabela_final.add_column("Título de Eleitor", style="bright_white")
    tabela_final.add_column("Mesário",           justify="center")
    tabela_final.add_column("Status de Votação", justify="center")
    tabela_final.add_column("Chave de Acesso",   style="bold yellow")

    mesario_texto = "[bold green]Sim[/bold green]" if eleitor['mesario'] else "[dim]Não[/dim]"
    tabela_final.add_row(
        str(eleitor['id']), eleitor['nome'], eleitor['titulo_eleitor'],
        mesario_texto, "[dim]Não Votou[/dim]", chave_acesso_original
    )
    console.print(Align.center(tabela_final))

    cursor.close()
    conexao.close()
    confirmacao.confirmacao()
    return True
