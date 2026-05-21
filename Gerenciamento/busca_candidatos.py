from database import conexao_banco as conect
from Validadores import confirmacao, gerenciador_de_entrada as ge, validacao_candidato as val_cand
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box
from Visual.visual import limpar_tela

console = Console(highlight=False)


def exibir_tabela_candidato(candidato):
    tabela = Table(
        title="Candidato Encontrado",
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


def busca_candidato():
    limpar_tela()

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    conteudo = (
        "[bold bright_white][1][/bold bright_white]  Buscar por Número de Votação\n"
        "[bold bright_white][2][/bold bright_white]  Buscar por Nome\n"
        "[dim]──────────────────────────────[/dim]\n"
        "[dim][X]  Cancelar[/dim]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]BUSCAR CANDIDATOS[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))

    opcao = ge.obter_entrada_inteira_valida("Digite uma opção: ", 1, 2)

    if opcao == False:
        cursor.close()
        conexao.close()
        return

    while opcao != 3:

        if opcao == 1:
            numero = ge.input_cancelavel("Digite o Número de Votação", "BUSCA POR NÚMERO")
            if numero is None:
                break
            while not val_cand.validacao_numero_votacao(numero):
                numero = ge.input_cancelavel("Número inválido. Digite novamente", "BUSCA POR NÚMERO")
                if numero is None:
                    break
            if numero is None:
                break

            cursor.execute("SELECT * FROM candidatos WHERE numero_votacao = %s", (numero,))
            candidato = cursor.fetchone()
            if candidato is not None:
                exibir_tabela_candidato(candidato)
            else:
                console.print("\n*** Candidato não encontrado! ***", style="bold yellow")

        if opcao == 2:
            nome = ge.input_cancelavel("Digite o Nome do Candidato", "BUSCA POR NOME")
            if nome is None:
                break

            cursor.execute("SELECT * FROM candidatos WHERE nome LIKE %s", (f"%{nome}%",))
            resultados = cursor.fetchall()
            if resultados:
                for candidato in resultados:
                    exibir_tabela_candidato(candidato)
            else:
                console.print("\n*** Candidato não encontrado! ***", style="bold yellow")

        break

    confirmacao.confirmacao()
    cursor.close()
    conexao.close()
