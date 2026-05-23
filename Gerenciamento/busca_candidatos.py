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
    """
    Exibe uma tabela estilizada no terminal com as informações detalhadas de um candidato.

    A função utiliza a biblioteca Rich para renderizar uma tabela centralizada
    contendo os dados de um candidato específico que foi localizado no sistema.

    Args:
        candidato (dict): Um dicionário contendo os dados do candidato extraídos do
        banco de dados. Deve obrigatoriamente possuir as seguintes chaves:
        - 'id' (int ou str): O identificador único do candidato.
        - 'nome' (str): O nome completo do candidato.
        - 'partido' (str): O nome do partido político.
        - 'sigla_partido' (str): A sigla do partido.
        - 'numero_votacao' (str ou int): O número do candidato na urna.

    Returns:
        None: A função realiza apenas a impressão dos dados no terminal, sem retornar valor.
        """
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
    """
    Gerencia a interface interativa para pesquisa de candidatos no sistema.

    A função abre um menu que permite ao usuário escolher entre dois métodos de
    busca distintos:

    1.  Por Número de Votação: Realiza uma busca exata por um número previamente
        validado e exibe o candidato correspondente.
    2.  Por Nome: Realiza uma busca parcial (utilizando o operador LIKE do SQL),
        permitindo encontrar e listar múltiplos candidatos que contenham o termo digitado.

    Em ambos os casos, se houver resultados, eles serão renderizados em formato
    de tabela na tela. Caso contrário, uma mensagem informando que nenhum candidato
    foi localizado será exibida. A operação pode ser cancelada pelo usuário a
    qualquer momento.

    Args:
        None.

    Returns:
        None: A função manipula diretamente as saídas no console e encerra conexões,
        não retornando nenhum valor.
    """
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

    if not opcao:
        cursor.close()
        conexao.close()
        return

    while opcao == 1 or opcao == 2:

        if opcao == 1:
            limpar_tela()
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
                limpar_tela()
                exibir_tabela_candidato(candidato)
            else:
                limpar_tela()
                console.print("\n*** Candidato não encontrado! ***", style="bold yellow")

        if opcao == 2:
            limpar_tela()
            nome = ge.input_cancelavel("Digite o Nome do Candidato", "BUSCA POR NOME")
            if nome is None:
                break

            cursor.execute("SELECT * FROM candidatos WHERE nome LIKE %s", (f"%{nome}%",))
            resultados = cursor.fetchall()
            if resultados:
                for candidato in resultados:
                    limpar_tela()
                    exibir_tabela_candidato(candidato)
            else:
                limpar_tela()
                console.print("\n*** Candidato não encontrado! ***", style="bold yellow")

        break

    confirmacao.confirmacao()
    cursor.close()
    conexao.close()
