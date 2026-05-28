from database import conexao_banco as conect
from Validadores import confirmacao as conf, gerenciador_de_entrada as ge, validacao_cpf as val_cpf, validacao_titulo as val_tit
from criptografia import criptografia as crip
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box
from Visual.visual import limpar_tela

console = Console(highlight=False)

def exibir_tabela_eleitor(eleitor):
    """
    Exibe uma tabela estilizada no terminal com as informações do eleitor selecionado para remoção.

    Utiliza a biblioteca Rich para criar e renderizar uma tabela centralizada,
    permitindo que o usuário valide visualmente os dados do eleitor (ID, Nome,
    Título, se é Mesário e Status de Votação) antes de prosseguir com a exclusão definitiva.

    Args:
        eleitor (dict): Dicionário contendo os dados do eleitor extraídos do
        banco de dados. Deve possuir as chaves obrigatórias: 'id', 'nome',
        'titulo_eleitor', 'mesario' e 'status_votacao'.

    Returns:
        None: A função realiza apenas a impressão dos dados no terminal, sem retornar valor.
        """

    mesario_texto = "[bold green]Sim[/bold green]" if eleitor['mesario'] == 1 else "[red]Não[/red]"
    status_texto  = "[bold green]Já Votou[/bold green]" if eleitor['status_votacao'] == 1 else "[red]Não Votou[/red]"

    tabela = Table(
        title="Eleitor a ser Removido",
        box=box.DOUBLE,
        border_style="bold #D4620A",
        title_style="bold bright_white",
        header_style="bold #D4620A",
        show_lines=True
    )
    tabela.add_column("ID",                justify="center", style="bright_white")
    tabela.add_column("Nome",              style="bright_white")
    tabela.add_column("Título de Eleitor", style="bright_white")
    tabela.add_column("Mesário",           justify="center")
    tabela.add_column("Status de Votação", justify="center")

    tabela.add_row(str(eleitor['id']), eleitor['nome'], eleitor['titulo_eleitor'], mesario_texto, status_texto)
    console.print(Align.center(tabela))

def remocao_eleitores():
    """
    Gerencia a interface interativa e executa a exclusão de eleitores do banco de dados.

    A função abre um menu de opções para localizar o eleitor que será removido,
    permitindo dois tipos de filtros:

    1. Por CPF: O input é validado e criptografado para conferência e busca na tabela.

    2. Por Título de Eleitor: O input é validado e consultado diretamente de forma textual.

    Caso o eleitor seja localizado, a tabela com suas informações é exibida e um
    painel de confirmação é gerado. Se o usuário confirmar a ação (Opção 1), o comando
    SQL DELETE é executado baseado no ID único do eleitor e consolidado com um commit.
    Se o usuário cancelar ou se o eleitor não for encontrado, o fluxo fecha as conexões
    com segurança e encerra a rotina.

    Args:
        None.

    Returns:
        bool ou None: Retorna False de forma imediata caso o usuário cancele a operação
        logo na seleção inicial do menu. Retorna None ao concluir a execução normal da
        exclusão, cancelamento interno ou término das rotinas.
    """

    limpar_tela()

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    conteudo = (
        "[bold bright_white][1][/bold bright_white]  Remover pelo CPF\n"
        "[bold bright_white][2][/bold bright_white]  Remover pelo Título de Eleitor\n"
        "[dim]──────────────────────────────[/dim]\n"
        "[red][X]  Cancelar[/red]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]EXCLUIR ELEITORES[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))

    opcao = ge.obter_entrada_inteira_valida("Digite uma opção: ", 1, 2)

    if not opcao:
        cursor.close()
        conexao.close()
        return False

    eleitor = None

    if opcao == 1:
        limpar_tela()
        cpf = ge.input_cancelavel("Digite o CPF do eleitor a ser removido", "REMOVER POR CPF")
        if cpf is not None:
            while not val_cpf.validacao_de_cpf(cpf):
                cpf = ge.input_cancelavel("CPF inválido. Digite novamente", "REMOVER POR CPF")
                if cpf is None:
                    break
            if cpf is not None:
                cpf_criptografado = crip.criptografar_cpf(cpf)
                cursor.execute('SELECT * FROM eleitores WHERE cpf = %s', (cpf_criptografado,))
                eleitor = cursor.fetchone()
                if eleitor is None:
                    limpar_tela()
                    console.print("\nEleitor não cadastrado.", style="bold yellow")
                    input("\nPressione Enter para continuar inserir novamente...")

    elif opcao == 2:
        limpar_tela()
        titulo_eleitor = ge.input_cancelavel("Digite o Título de Eleitor a ser removido", "REMOVER POR TÍTULO")
        if titulo_eleitor is not None:
            while not val_tit.validar_titulo(titulo_eleitor):
                titulo_eleitor = ge.input_cancelavel("Título inválido. Digite novamente", "REMOVER POR TÍTULO")
                if titulo_eleitor is None:
                    break
            if titulo_eleitor is not None:
                titulo_eleitor = titulo_eleitor.replace(" ", "")
                cursor.execute('SELECT * FROM eleitores WHERE titulo_eleitor = %s', (titulo_eleitor,))
                eleitor = cursor.fetchone()
                if eleitor is None:
                    limpar_tela()
                    console.print("\nEleitor não cadastrado.", style="bold yellow")
                    input("\nPressione Enter para continuar inserir novamente...")

    if eleitor is not None:
        limpar_tela()
        exibir_tabela_eleitor(eleitor)

        conteudo_remover = (
            "[bold bright_white][1][/bold bright_white]  Sim\n"
            "[dim]──────────────────────────────[/dim]\n"
            "[red][2]  Não[/red]"
        )
        console.print(Panel(Align.center(conteudo_remover), title="[bold bright_white]CONFIRMAR REMOÇÃO[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))
        confirmacao = ge.obter_entrada_inteira_valida("Opção escolhida: ", 1, 2)

        if confirmacao == 1:
            limpar_tela()
            cursor.execute('DELETE FROM eleitores WHERE id = %s', (eleitor['id'],))
            conexao.commit()
            console.print("\nEleitor removido com sucesso.", style="bold green")
            conf.confirmacao()
        else:
            limpar_tela()
            console.print("\nRemoção cancelada pelo usuário.", style="bold yellow")
            conf.confirmacao()

    cursor.close()
    conexao.close()
    return None
