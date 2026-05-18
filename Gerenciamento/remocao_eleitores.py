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

    mesario_texto = "[bold green]Sim[/bold green]" if eleitor['mesario'] == 1 else "[dim]Não[/dim]"
    status_texto  = "[bold green]Já Votou[/bold green]" if eleitor['status_votacao'] == 1 else "[dim]Não Votou[/dim]"

    tabela = Table(
        title="Eleitor a ser Removido",
        box=box.DOUBLE,
        border_style="bold sandy_brown",
        title_style="bold bright_white",
        header_style="bold sandy_brown",
        show_lines=True
    )
    tabela.add_column("ID",                justify="center", style="bright_white")
    tabela.add_column("Nome",              style="bright_white")
    tabela.add_column("Título de Eleitor", style="bright_white")
    tabela.add_column("Mesário",           justify="center")
    tabela.add_column("Status de Votação", justify="center")

    tabela.add_row(str(eleitor['id']), eleitor['nome'], eleitor['titulo_eleitor'], mesario_texto, status_texto)
    console.print(tabela)

def remocao_eleitores():
    """
    A função exibe opções para receber valores str de cpf ou titulo de eleitor para remoção do eleitor no banco de dados.
    Utiliza de funções de criptografia, validação e gerenciamento de entrada.

    Args:
        none

    Returns:
        Exibe (print) os dados do eleitor a ser removido na tela para o usuário.
        Realiza a exclusão do eleitor no banco de dados após confirmação.
        Exibe opções de novas remoções ou troca de Menu.
    """

    limpar_tela()

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    conteudo = (
        "[bold bright_white][1][/bold bright_white]  Remover pelo CPF\n"
        "[bold bright_white][2][/bold bright_white]  Remover pelo Título de Eleitor\n"
        "[dim]──────────────────────────────[/dim]\n"
        "[dim][X]  Cancelar[/dim]"
    )
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]EXCLUIR ELEITORES[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))

    opcao = ge.obter_entrada_inteira_valida("Digite uma opção: ", 1, 2)

    if opcao == False:
        return False

    while opcao != 3:
        eleitor = None

        match opcao:
            case 1:
                cpf = str(input("\nDigite o número do CPF a ser removido: "))
                validacao_cpf = val_cpf.validacao_de_cpf(cpf)

                if validacao_cpf == True:
                    cpf_criptografado = crip.criptografar_cpf(cpf)
                    cursor.execute('SELECT * FROM eleitores WHERE cpf = %s', (cpf_criptografado,))
                    eleitor = cursor.fetchone()

                    if eleitor is None:
                        console.print("\nEleitor não cadastrado.", style="bold yellow")
                else:
                    console.print("\nPor favor, refaça sua busca!", style="bold yellow")

            case 2:
                titulo_eleitor = str(input("\nDigite o número do Título de Eleitor a ser removido: "))

                if val_tit.validar_titulo(titulo_eleitor):
                    cursor.execute('SELECT * FROM eleitores WHERE titulo_eleitor = %s', (titulo_eleitor,))
                    eleitor = cursor.fetchone()

                    if eleitor is None:
                        console.print("\nEleitor não cadastrado.", style="bold yellow")
                else:
                    console.print("\nTítulo de Eleitor inválido. Por favor, refaça sua busca!")

        if eleitor is not None:
            exibir_tabela_eleitor(eleitor)

            console.print("\nDeseja realmente remover este eleitor?\n 1 - Sim\n 2 - Não")
            confirmacao = ge.obter_entrada_inteira_valida("Opção escolhida: ", 1, 2)

            if confirmacao == 1:
                cursor.execute('DELETE FROM eleitores WHERE id = %s', (eleitor['id'],))
                conexao.commit()
                console.print("\nEleitor removido com sucesso.", style="bold green")
                conf.confirmacao()
                break
            else:
                console.print("\nRemoção cancelada pelo usuário.", style="bold yellow")
                conf.confirmacao()
                break

    cursor.close()
    conexao.close()
