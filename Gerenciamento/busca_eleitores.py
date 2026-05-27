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
    """
    Exibe uma tabela estilizada no terminal com os dados detalhados do eleitor encontrado.

    A tabela é gerada dinamicamente utilizando a biblioteca Rich. Caso o parâmetro
    'cpf' seja fornecido, a função adiciona uma coluna extra para renderizar este
    dado. Os status de mesário e de votação recebem cores e formatações específicas
    (Verde para ativo/concluído e esmaecido para falso/pendente).

    Args:
        id_ (int ou str): O identificador único do eleitor no banco de dados.
        nome (str): O nome completo do eleitor.
        titulo_eleitor (str): O número do título de eleitor.
        mesario (int ou bool): Flag indicando se o eleitor é mesário (1 ou True) ou não.
        status_votacao (int ou bool): Flag indicando se o eleitor já votou (1 ou True) ou não.
        cpf (str, optional): O CPF em formato limpo do eleitor. Se omitido, a coluna CPF
        não será gerada na tabela. O padrão é None.

    Returns:
        None: A função realiza apenas a impressão dos dados no terminal, sem retornar valor.
        """

    mesario_texto  = "[bold green]Sim[/bold green]" if mesario == 1 else "[red]Não[/red]"
    status_texto   = "[bold green]Já Votou[/bold green]" if status_votacao == 1 else "[red]Não Votou[/red]"

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
    console.print(Align.center(tabela))

def busca_eleitor():
    """
    Gerencia a interface interativa de pesquisa e consulta de eleitores cadastrados.

    A função apresenta um menu de opções no terminal que permite localizar um
    eleitor utilizando dois critérios de pesquisa:

    1. Pelo CPF: O valor digitado é validado, criptografado para comparação e,
       se encontrado, exibe a tabela contendo o CPF aberto inserido pelo usuário.
    2. Pelo Título de Eleitor: O valor digitado é validado e pesquisado diretamente
       no banco de dados.

    Caso o eleitor não conste na base de dados, uma mensagem orientando a realização
    do cadastro no Menu de Gerenciamento é exibida. O fluxo fecha corretamente
    os cursores e conexões com o banco antes de finalizar.

    Args:
        None.

    Returns:
        bool ou None: Retorna False de forma imediata caso o usuário decida cancelar
        a operação logo na seleção inicial do menu. Retorna None após a execução normal
        da pesquisa ou cancelamento nas etapas internas de input.
    """
    limpar_tela()

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    conteudo = (
        "[bold bright_white][1][/bold bright_white]  Buscar pelo CPF\n"
        "[bold bright_white][2][/bold bright_white]  Buscar pelo Título de Eleitor\n"
        "[dim]──────────────────────────────[/dim]\n"
        "[red][X]  Cancelar[/red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]BUSCAR ELEITORES[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))

    opcao = ge.obter_entrada_inteira_valida("Digite uma opção: ", 1, 2)

    if not opcao:
        cursor.close()
        conexao.close()
        return False

    if opcao == 1:
        limpar_tela()
        cpf = ge.input_cancelavel("Digite o CPF do eleitor", "BUSCA POR CPF")
        if cpf is not None:
            while not val_cpf.validacao_de_cpf(cpf):
                limpar_tela()
                cpf = ge.input_cancelavel("CPF inválido. Digite novamente", "BUSCA POR CPF")
                if cpf is None:
                    limpar_tela()
                    break
            if cpf is not None:
                cpf = cpf.replace(" ", "")
                cpf_criptografado = cripto.criptografar_cpf(cpf)
                if ver_cpf.verificar_cpf_banco(cpf_criptografado)[0] == 1:
                    cursor.execute(
                        "SELECT id, nome, titulo_eleitor, mesario, status_votacao FROM eleitores WHERE cpf = %s",
                        (cpf_criptografado,)
                    )
                    e = cursor.fetchone()
                    limpar_tela()
                    exibir_tabela_eleitor(e['id'], e['nome'], e['titulo_eleitor'], e['mesario'], e['status_votacao'], cpf=cpf)
                else:
                    limpar_tela()
                    console.print("\n*** Eleitor não cadastrado! ***\nRealizar o cadastramento no Menu Gerenciamento de Eleitores.", style="bold yellow")

    elif opcao == 2:
        limpar_tela()
        titulo_eleitor = ge.input_cancelavel("Digite o Título de Eleitor", "BUSCA POR TÍTULO")
        if titulo_eleitor is not None:
            while not val_titulo.validar_titulo(titulo_eleitor):
                limpar_tela()
                titulo_eleitor = ge.input_cancelavel("Título inválido. Digite novamente", "BUSCA POR TÍTULO")
                if titulo_eleitor is None:
                    limpar_tela()
                    break
            if titulo_eleitor is not None:
                titulo_eleitor = titulo_eleitor.replace(" ", "")
                if ver_titulo.verificar_titulo_de_eleitor_banco(titulo_eleitor)[0] == 1:
                    cursor.execute(
                        "SELECT id, nome, titulo_eleitor, mesario, status_votacao FROM eleitores WHERE titulo_eleitor = %s",
                        (titulo_eleitor,)
                    )
                    e = cursor.fetchone()
                    limpar_tela()
                    exibir_tabela_eleitor(e['id'], e['nome'], e['titulo_eleitor'], e['mesario'], e['status_votacao'])
                else:
                    limpar_tela()
                    console.print("*** Eleitor não cadastrado! ***\nRealizar o cadastramento no Menu Gerenciamento de Eleitores.\n", style="bold yellow")

    confirmacao.confirmacao()
    cursor.close()
    conexao.close()
    return None
