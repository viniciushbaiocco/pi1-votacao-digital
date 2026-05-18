import database.conexao_banco as conect
import Validadores.gerenciador_de_entrada as ge
import Validadores.validacao_cpf as val_cpf
import Validadores.validacao_titulo as val_titulo
import Verificadores.verificacao_cpf_banco as ver_cpf
import Verificadores.verificacao_titulo_banco as ver_titulo
import criptografia.criptografia as cripto
from Validadores import confirmacao
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box
from Visual.visual import limpar_tela

console = Console(highlight=False)

def exibir_tabela_eleitor(id_, nome, titulo_eleitor, mesario, status_votacao, cpf=None):

    mesario_texto  = "[bold green]Sim[/bold green]" if mesario == 1 else "[dim]Não[/dim]"
    status_texto   = "[bold green]Já Votou[/bold green]" if status_votacao == 1 else "[dim]Não Votou[/dim]"

    tabela = Table(
        title="Eleitor Encontrado",
        box=box.DOUBLE,
        border_style="bold sandy_brown",
        title_style="bold bright_white",
        header_style="bold sandy_brown",
        show_lines=True
    )
    tabela.add_column("ID",                justify="center", style="bright_white")
    tabela.add_column("Nome",              style="bright_white")
    if cpf is not None:
        tabela.add_column("CPF",           style="bright_white")
    tabela.add_column("Título de Eleitor", style="bright_white")
    tabela.add_column("Mesário",           justify="center")
    tabela.add_column("Status de Votação", justify="center")

    if cpf is not None:
        tabela.add_row(str(id_), nome, cpf, titulo_eleitor, mesario_texto, status_texto)
    else:
        tabela.add_row(str(id_), nome, titulo_eleitor, mesario_texto, status_texto)
    console.print(tabela)

def busca_eleitor():
    """
    A função exibe opções para receber valores str de cpf ou titulo de eleitor para consulta do eleitor no banco de dados.
    Utiliza de funções de criptografia, validacao e verificacao de CPF e título de eleitor.

    Args:
        none

    Returns:
        Exibe os dados selecionados do eleitor na tela para o usuário.
    """
    limpar_tela()

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    conteudo = (
        "[bold bright_white][1][/bold bright_white]  Buscar pelo CPF\n"
        "[bold bright_white][2][/bold bright_white]  Buscar pelo Título de Eleitor\n"
        "[dim]──────────────────────────────[/dim]\n"
        "[dim][X]  Cancelar[/dim]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]BUSCAR ELEITORES[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))

    opcao = ge.obter_entrada_inteira_valida("Digite uma opção: ", 1, 2)

    if opcao == False:
        return False

    while opcao != 3:

        if opcao == 1:
            cpf = ge.input_cancelavel("Digite o CPF do eleitor", "BUSCA POR CPF")
            if cpf is None:
                break
            while val_cpf.validacao_de_cpf(cpf) == False:
                cpf = ge.input_cancelavel("CPF inválido. Digite novamente", "BUSCA POR CPF")
                if cpf is None:
                    break
            if cpf is None:
                break

            cpf_criptografado = cripto.criptografar_cpf(cpf)
            if ver_cpf.verificar_cpf_banco(cpf_criptografado)[0] == 1:
                cursor.execute(
                    "SELECT id, nome, titulo_eleitor, mesario, status_votacao FROM eleitores WHERE cpf = %s",
                    (cpf_criptografado,)
                )
                e = cursor.fetchone()
                exibir_tabela_eleitor(e['id'], e['nome'], e['titulo_eleitor'], e['mesario'], e['status_votacao'], cpf=cpf)
            else:
                console.print("\n*** Eleitor não cadastrado! ***\nRealizar o cadastramento no Menu Gerenciamento de Eleitores.", style="bold yellow")

        if opcao == 2:
            titulo_eleitor = ge.input_cancelavel("Digite o Título de Eleitor", "BUSCA POR TÍTULO")
            if titulo_eleitor is None:
                break
            while val_titulo.validar_titulo(titulo_eleitor) == False:
                titulo_eleitor = ge.input_cancelavel("Título inválido. Digite novamente", "BUSCA POR TÍTULO")
                if titulo_eleitor is None:
                    break
            if titulo_eleitor is None:
                break

            if ver_titulo.verificar_titulo_de_eleitor_banco(titulo_eleitor)[0] == 1:
                cursor.execute(
                    "SELECT id, nome, titulo_eleitor, mesario, status_votacao FROM eleitores WHERE titulo_eleitor = %s",
                    (titulo_eleitor,)
                )
                e = cursor.fetchone()
                exibir_tabela_eleitor(e['id'], e['nome'], e['titulo_eleitor'], e['mesario'], e['status_votacao'])
            else:
                console.print("*** Eleitor não cadastrado! ***\nRealizar o cadastramento no Menu Gerenciamento de Eleitores.\n", style="bold yellow")
        break

    confirmacao.confirmacao()
    cursor.close()
    conexao.close()
