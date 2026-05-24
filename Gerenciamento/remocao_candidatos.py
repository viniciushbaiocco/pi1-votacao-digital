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
    Exibe uma tabela estilizada no terminal com os dados do candidato a ser removido.

    Utiliza a biblioteca Rich para renderizar uma tabela centralizada, permitindo que
    o usuário confira os dados do candidato (ID, Nome, Partido, Sigla e Número de Votação)
    antes de confirmar a exclusão.

    Args:
        candidato (dict): Dicionário com os dados do candidato extraídos do banco de
        dados. Deve possuir as chaves: 'id', 'nome', 'partido', 'sigla_partido' e
        'numero_votacao'.

    Returns:
        None: A função realiza apenas a impressão dos dados no terminal, sem retornar valor.
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
    """
    Gerencia a interface de exclusão e remove candidatos da base de dados.

    A função interage com o usuário para obter o número eleitoral do candidato que
    deseja remover. O processo segue um fluxo estrito de validação e segurança:

    1.  Solicita e valida a sintaxe do número de votação informado.
    2.  Consulta o banco para obter o registro correspondente.
    3.  Aplica uma regra de negócio impeditiva: se o candidato consultado for o
        'Voto Nulo' (número '00'), a remoção é negada por se tratar de um registro
        estrutural obrigatório do sistema da urna.
    4.  Exibe a tabela com os dados do candidato e exige uma confirmação explícita
        antes de rodar o comando SQL `DELETE` com base no ID único do registro.

    A função garante o encerramento dos cursores e conexões abertas com o MySQL em todos
    os pontos de interrupção ou retornos antecipados.

    Args:
        None.

    Returns:
        None: A função gerencia entradas, interações na CLI e mutações na base de dados,
        encerrando a execução por meio de retornos vazios (`return`).
    """
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
        limpar_tela()
        console.print("\nO candidato de voto nulo é estrutural do sistema e não pode ser removido.", style="bold red")
        conf.confirmacao()
        cursor.close()
        conexao.close()
        return

    limpar_tela()
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
        limpar_tela()
        console.print("\nCandidato removido com sucesso.", style="bold green")
    else:
        limpar_tela()
        console.print("\nRemoção cancelada pelo usuário.", style="bold yellow")

    conf.confirmacao()
    cursor.close()
    conexao.close()
