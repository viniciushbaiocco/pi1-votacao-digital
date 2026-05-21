from database import conexao_banco as conect
from Validadores import confirmacao, gerenciador_de_entrada as ge, validacao_candidato as val_cand, validacao_nome as val_nome, validacao_partido as val_partido
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box
from Visual.visual import limpar_tela
from time import sleep

console = Console(highlight=False)


def exibir_tabela_candidato(titulo, candidato):
    tabela = Table(
        title=titulo,
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


def edicao_candidatos():
    limpar_tela()

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    numero = ge.input_cancelavel("Digite o Número de Votação do candidato a ser editado", "EDITAR CANDIDATO")
    if numero is None:
        cursor.close()
        conexao.close()
        return

    while not val_cand.validacao_numero_votacao(numero):
        numero = ge.input_cancelavel("Número inválido. Digite novamente", "EDITAR CANDIDATO")
        if numero is None:
            cursor.close()
            conexao.close()
            return

    cursor.execute("SELECT * FROM candidatos WHERE numero_votacao = %s", (numero,))
    candidato = cursor.fetchone()

    if candidato is None:
        console.print("\n*** Candidato não encontrado! ***", style="bold yellow")
        confirmacao.confirmacao()
        cursor.close()
        conexao.close()
        return

    if candidato['numero_votacao'] == '00':
        console.print("\nO candidato de voto nulo é estrutural do sistema e não pode ser editado.", style="bold red")
        sleep(1.5)
        confirmacao.confirmacao()
        cursor.close()
        conexao.close()
        return

    id_candidato = candidato['id']
    exibir_tabela_candidato("Candidato a Ser Editado", candidato)

    conteudo_confirmar = (
        "[bold bright_white][1][/bold bright_white]  Sim\n"
        "[dim]──────────────────────────────[/dim]\n"
        "[dim][2]  Não[/dim]"
    )
    console.print(Panel(Align.center(conteudo_confirmar), title="[bold bright_white]CONFIRMAR EDIÇÃO[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))
    opcao_confirmar = ge.obter_entrada_inteira_valida('\nDigite uma opção: ', 1, 2)

    if opcao_confirmar != 1:
        confirmacao.confirmacao()
        cursor.close()
        conexao.close()
        return

    editado = 0
    opcao_editar = 0
    while opcao_editar != 5:
        conteudo_campos = (
            "[bold bright_white][1][/bold bright_white]  Nome\n"
            "[bold bright_white][2][/bold bright_white]  Partido\n"
            "[bold bright_white][3][/bold bright_white]  Sigla do Partido\n"
            "[bold bright_white][4][/bold bright_white]  Número de Votação\n"
            "[dim]──────────────────────────────[/dim]\n"
            "[bold bright_white][5][/bold bright_white]  Confirmar\n"
            "[dim red][X]  Cancelar[/dim red]"
        )
        console.print(Panel(Align.center(conteudo_campos), title="[bold bright_white]O QUE DESEJA EDITAR[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))
        opcao_editar = ge.obter_entrada_inteira_valida('\nDigite uma opção: ', 1, 5)

        match opcao_editar:
            case 1:
                novo_nome = val_nome.validar_nome()
                if novo_nome is None:
                    continue
                if novo_nome == candidato['nome']:
                    console.print("Nome igual ao atual. Nenhuma alteração feita.", style="bold yellow")
                    sleep(1.5)
                    continue
                editado = 1
                cursor.execute('UPDATE candidatos SET nome = %s WHERE id = %s', (novo_nome, id_candidato))
                conexao.commit()
                console.print('Nome Editado Com Sucesso!', style="bold green")

            case 2:
                novo_partido = ge.input_cancelavel("Novo nome do Partido", "EDITAR PARTIDO")
                if novo_partido is None:
                    continue
                while not val_partido.validacao_partido(novo_partido):
                    novo_partido = ge.input_cancelavel("Partido inválido. Digite novamente", "EDITAR PARTIDO")
                    if novo_partido is None:
                        break
                if novo_partido is None:
                    continue
                if novo_partido == candidato['partido']:
                    console.print("Partido igual ao atual. Nenhuma alteração feita.", style="bold yellow")
                    sleep(1.5)
                    continue
                editado = 1
                cursor.execute('UPDATE candidatos SET partido = %s WHERE id = %s', (novo_partido, id_candidato))
                conexao.commit()
                console.print("Partido Editado Com Sucesso!", style="bold green")

            case 3:
                nova_sigla = ge.input_cancelavel("Nova Sigla do Partido", "EDITAR SIGLA")
                if nova_sigla is None:
                    continue
                nova_sigla = nova_sigla.upper()
                while not val_cand.validacao_sigla_partido(nova_sigla):
                    nova_sigla = ge.input_cancelavel("Sigla inválida. Digite novamente", "EDITAR SIGLA")
                    if nova_sigla is None:
                        break
                    nova_sigla = nova_sigla.upper()
                if nova_sigla is None:
                    continue
                if nova_sigla == candidato['sigla_partido']:
                    console.print("Sigla igual à atual. Nenhuma alteração feita.", style="bold yellow")
                    sleep(1.5)
                    continue
                editado = 1
                cursor.execute('UPDATE candidatos SET sigla_partido = %s WHERE id = %s', (nova_sigla, id_candidato))
                conexao.commit()
                console.print("Sigla Editada Com Sucesso!", style="bold green")

            case 4:
                novo_numero = ge.input_cancelavel("Novo Número de Votação", "EDITAR NÚMERO")
                if novo_numero is None:
                    continue
                while not val_cand.validacao_numero_votacao(novo_numero):
                    novo_numero = ge.input_cancelavel("Número inválido. Digite novamente", "EDITAR NÚMERO")
                    if novo_numero is None:
                        break
                if novo_numero is None:
                    continue
                if novo_numero == '00':
                    console.print("O número 00 é reservado para votos nulos.", style="bold red")
                    sleep(1.5)
                    continue
                if novo_numero == candidato['numero_votacao']:
                    console.print("Número igual ao atual. Nenhuma alteração feita.", style="bold yellow")
                    sleep(1.5)
                    continue
                cursor.execute("SELECT COUNT(*) as cnt FROM candidatos WHERE numero_votacao = %s", (novo_numero,))
                if cursor.fetchone()['cnt'] >= 1:
                    console.print("Número de Votação já em uso.", style="bold yellow")
                    sleep(1.5)
                    continue
                editado = 1
                cursor.execute('UPDATE candidatos SET numero_votacao = %s WHERE id = %s', (novo_numero, id_candidato))
                conexao.commit()
                console.print("Número de Votação Editado Com Sucesso!", style="bold green")

            case 5:
                if editado == 1:
                    cursor.execute('SELECT * FROM candidatos WHERE id = %s', (id_candidato,))
                    candidato = cursor.fetchone()
                    exibir_tabela_candidato("Candidato Após Edição", candidato)
                else:
                    console.print("Encerrando Operação...", style="bold yellow")

            case False:
                break

    cursor.close()
    conexao.close()
    return confirmacao.confirmacao()
