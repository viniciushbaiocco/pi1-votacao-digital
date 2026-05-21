from database import conexao_banco as conect
from Validadores import confirmacao as conf, gerenciador_de_entrada as ge, validacao_candidato as val_cand
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box
from Visual.visual import limpar_tela

console = Console(highlight=False)


def exibir_tabela_candidato(candidato):
    """
    Gerencia a interface interativa e executa a exclusão de candidatos no sistema.

    A função localiza o candidato no banco de dados por meio do número de votação.
    Garante a integridade do sistema impedindo estritamente a remoção do candidato
    com número '00' (reservado para computação de votos nulos).

    Caso o candidato seja elegível para remoção, seus dados são exibidos em uma tabela
    e um painel de confirmação é apresentado. Se o usuário confirmar a operação, o
    registro é deletado permanentemente via comando SQL DELETE e as alterações são
    consolidadas com um commit. Caso contrário, a ação é abortada com segurança.

    Args:
        None.

    Returns:
        None: A função gerencia entradas e saídas no terminal e interações com a
        base de dados, encerrando seus fluxos locais por meio de retornos antecipados.
    """
    tabela = Table(
        title="Candidato a ser Removido",
        box=box.DOUBLE,
        border_style="bold sandy_brown",
        title_style="bold bright_white",
        header_style="bold sandy_brown",
        show_lines=True
    )
    tabela.add_column("ID",               justify="center", style="bright_white")
    tabela.add_column("Nome",              style="bright_white")
    tabela.add_column("Partido",           style="bright_white")
    tabela.add_column("Sigla",             justify="center", style="bright_white")
    tabela.add_column("Número de Votação", justify="center", style="bright_white")

    tabela.add_row(
        str(candidato['id']),
        candidato['nome'],
        candidato['partido'],
        candidato['sigla_partido'],
        candidato['numero_votacao']
    )
    console.print(Align.center(tabela))


def remocao_candidatos():
    limpar_tela()

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    numero = ge.input_cancelavel("Digite o Número de Votação do candidato a ser removido", "EXCLUIR CANDIDATO")
    if numero is None:
        cursor.close()
        conexao.close()
        return

    while not val_cand.validacao_numero_votacao(numero):
        numero = ge.input_cancelavel("Número inválido. Digite novamente", "EXCLUIR CANDIDATO")
        if numero is None:
            cursor.close()
            conexao.close()
            return

    cursor.execute("SELECT * FROM candidatos WHERE numero_votacao = %s", (numero,))
    candidato = cursor.fetchone()

    if candidato is None:
        console.print("\nCandidato não cadastrado.", style="bold yellow")
        conf.confirmacao()
        cursor.close()
        conexao.close()
        return

    if candidato['numero_votacao'] == '00':
        console.print("\nO candidato de voto nulo é estrutural do sistema e não pode ser removido.", style="bold red")
        conf.confirmacao()
        cursor.close()
        conexao.close()
        return

    exibir_tabela_candidato(candidato)

    conteudo_remover = (
        "[bold bright_white][1][/bold bright_white]  Sim\n"
        "[dim]──────────────────────────────[/dim]\n"
        "[dim][2]  Não[/dim]"
    )
    console.print(Panel(Align.center(conteudo_remover), title="[bold bright_white]CONFIRMAR REMOÇÃO[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))
    confirmacao = ge.obter_entrada_inteira_valida("Opção escolhida: ", 1, 2)

    if confirmacao == 1:
        cursor.execute("DELETE FROM candidatos WHERE id = %s", (candidato['id'],))
        conexao.commit()
        console.print("\nCandidato removido com sucesso.", style="bold green")
    else:
        console.print("\nRemoção cancelada pelo usuário.", style="bold yellow")

    conf.confirmacao()
    cursor.close()
    conexao.close()
