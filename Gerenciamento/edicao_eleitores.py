from database import conexao_banco as conect
from criptografia import criptografia as crip
from Verificadores import verificacao_cpf_banco as ver_cpf
from Verificadores import verificacao_titulo_banco as ver_tit
from Cadastro import chave_acesso as chave
from Validadores import confirmacao, gerenciador_de_entrada as ge, validacao_cpf as val_cpf, validacao_nome as val_nome, validacao_titulo as val_tit
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box
from Visual.visual import limpar_tela, carregar_pontos_loop
from time import sleep

console = Console(highlight=False)

def exibir_tabela_eleitor(titulo, eleitor):
    """
    Exibe uma tabela estilizada no terminal com as informações de um eleitor.

    A função reconstrói e renderiza uma tabela centralizada via biblioteca Rich.
    Durante o processo, ela descriptografa o CPF do eleitor em tempo de execução
    para exibi-lo em formato limpo e legível. Os status de mesário e votação são
    estilizados com cores dinâmicas (Verde/Esmaecido).

    Args:
        titulo (str): O título que será exibido no cabeçalho superior da tabela.
        eleitor (dict): Um dicionário contendo os dados do eleitor extraídos do
        banco de dados. Deve possuir as chaves: 'id', 'nome', 'cpf'
        (criptografado), 'titulo_eleitor', 'mesario' e 'status_votacao'.

    Returns:
        None: A função apenas manipula saídas no console, não retornando valor.
    """

    mesario_texto = "[bold green]Sim[/bold green]" if eleitor['mesario'] == 1 else "[dim]Não[/dim]"
    status_texto  = "[bold green]Já Votou[/bold green]" if eleitor['status_votacao'] == 1 else "[dim]Não Votou[/dim]"
    cpf_desc      = crip.descriptografar_cpf(eleitor['cpf'])

    tabela = Table(
        title=titulo,
        box=box.DOUBLE,
        border_style="bold sandy_brown",
        title_style="bold bright_white",
        header_style="bold sandy_brown",
        show_lines=True
    )
    tabela.add_column("ID", justify="center", style="bright_white")
    tabela.add_column("Nome",              style="bright_white")
    tabela.add_column("CPF",               style="bright_white")
    tabela.add_column("Título de Eleitor", style="bright_white")
    tabela.add_column("Mesário",           justify="center")
    tabela.add_column("Status de Votação", justify="center")

    tabela.add_row(str(eleitor['id']), eleitor['nome'], cpf_desc, eleitor['titulo_eleitor'], mesario_texto, status_texto)
    console.print(Align.center(tabela))

def edicao_eleitores():
    """
    Gerencia a interface interativa e as regras de alteração cadastral de eleitores.

    Permite localizar um eleitor ativo utilizando filtros por CPF ou por Título
    de Eleitor. Após a confirmação da identidade, abre um menu cíclico para a
    modificação pontual de dados cadastrais (Nome, Título, CPF ou Status de Mesário).

    Regras de negócio implementadas:

    1.  Alteração de Nome: Força a regeneração automática de uma nova chave de acesso
        exclusiva para a urna, imprimindo o novo token em destaque na tela.
    2.  Modificação de chaves únicas (CPF/Título): Valida contra duplicidades na
        base de dados e rejeita entradas idênticas às já armazenadas.
    3.  Proteção de dados: O CPF novo é criptografado antes da persistência.

    Args:
        None.

    Returns:
        Any: Retorna o resultado do módulo `confirmacao.confirmacao()` após a
        conclusão ou cancelamento das operações. Pode retornar None em caso de
        saída precoce nos inputs iniciais.
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
    console.print(Panel(Align.center(conteudo), title="[bold bright_white]EDITAR ELEITORES[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))

    opcao = ge.obter_entrada_inteira_valida("Digite uma opção: ", 1, 2)

    if not opcao:
        cursor.close()
        conexao.close()
        return None

    match opcao:
        case 1:
            limpar_tela()
            cpf = ge.input_cancelavel("Digite o CPF do eleitor a ser editado", "EDITAR POR CPF")
            if cpf is None:
                cursor.close(); conexao.close()
                return None
            while not val_cpf.validacao_de_cpf(cpf):
                cpf = ge.input_cancelavel("CPF inválido. Digite novamente", "EDITAR POR CPF")
                if cpf is None:
                    break
            if cpf is None:
                cursor.close(); conexao.close()
                return None

            cursor.execute('SELECT id FROM eleitores WHERE cpf = %s', (crip.criptografar_cpf(cpf),))
            if ver_cpf.verificar_cpf_banco(crip.criptografar_cpf(cpf)) == (0,):
                console.print("\n*** Eleitor não cadastrado! *** \nRealizar o cadastramento no Menu Gerenciamento de Eleitores.", style="bold yellow")
        case 2:
            limpar_tela()
            tit = ge.input_cancelavel("Digite o Título de Eleitor a ser editado", "EDITAR POR TÍTULO")
            if tit is None:
                cursor.close(); conexao.close()
                return None
            while not val_tit.validar_titulo(tit):
                tit = ge.input_cancelavel("Título inválido. Digite novamente", "EDITAR POR TÍTULO")
                if tit is None:
                    break
            if tit is None:
                cursor.close(); conexao.close()
                return None

            cursor.execute('SELECT id FROM eleitores WHERE titulo_eleitor = %s', (tit,))
            if ver_cpf.verificar_cpf_banco(tit) == (0,):
                console.print("\n*** Eleitor não cadastrado! *** \nRealizar o cadastramento no Menu Gerenciamento de Eleitores.", style="bold yellow")

    eleitor = cursor.fetchone()
    if eleitor is None:
        return confirmacao.confirmacao()
    id_eleitor = eleitor['id']

    cursor.execute('SELECT * FROM eleitores WHERE id = %s', (id_eleitor,))
    eleitor = cursor.fetchone()

    limpar_tela()
    exibir_tabela_eleitor("Eleitor a Ser Editado", eleitor)

    conteudo_confirmar = (
        "[bold bright_white][1][/bold bright_white]  Sim\n"
        "[dim]──────────────────────────────[/dim]\n"
        "[dim][2]  Não[/dim]"
    )
    console.print(Panel(Align.center(conteudo_confirmar), title="[bold bright_white]CONFIRMAR EDIÇÃO[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))
    opcao2 = ge.obter_entrada_inteira_valida('\nDigite uma opção: ', 1, 2)
    editado = 0
    match opcao2:
        case 1:
            limpar_tela()
            opcao_editar = 0
            while opcao_editar != 5:
                conteudo_campos = (
                    "[bold bright_white][1][/bold bright_white]  Nome\n"
                    "[bold bright_white][2][/bold bright_white]  Título\n"
                    "[bold bright_white][3][/bold bright_white]  CPF\n"
                    "[bold bright_white][4][/bold bright_white]  Mesário\n"
                    "[dim]──────────────────────────────[/dim]\n"
                    "[bold bright_white][5][/bold bright_white]  Confirmar"
                )
                console.print(Panel(Align.center(conteudo_campos), title="[bold bright_white]O QUE DESEJA EDITAR[/bold bright_white]", border_style="bold sandy_brown", box=box.DOUBLE, padding=(1, 4)))
                opcao_editar = ge.obter_entrada_inteira_valida('\nDigite uma opção: ', 1, 5)
                match opcao_editar:
                    case 1:
                        limpar_tela()
                        novo_nome = val_nome.validar_nome()
                        if novo_nome is None:
                            limpar_tela()
                            continue
                        nova_chave_acesso = chave.geracao_chave_acesso(novo_nome)
                        nova_chave_criptografada = crip.criptografar_chave_acesso(nova_chave_acesso)
                        editado = 1
                        cursor.execute('''
                        UPDATE eleitores SET nome = %s, chave_acesso = %s
                                            WHERE id = %s
                        ''', (novo_nome, nova_chave_criptografada, id_eleitor))
                        conexao.commit()
                        console.print('[bold green]\nNome Editado Com Sucesso![/bold green]')
                        console.print(f'\nNova Chave de Acesso é: [bold yellow]{nova_chave_acesso}[/bold yellow]')
                        confirmacao.confirmacao()
                        limpar_tela()
                    case 2:
                        limpar_tela()
                        novo_titulo = ge.input_cancelavel("Novo Título de Eleitor", "EDITAR TÍTULO")
                        if novo_titulo is None:
                            limpar_tela()
                            continue
                        while not val_tit.validar_titulo(novo_titulo):
                            novo_titulo = ge.input_cancelavel("Título inválido. Digite novamente", "EDITAR TÍTULO")
                            if novo_titulo is None:
                                limpar_tela()
                                break
                        if novo_titulo is None:
                            limpar_tela()
                            continue
                        if novo_titulo == eleitor['titulo_eleitor']:
                            console.print("Título igual ao atual. Nenhuma alteração feita.", style="bold yellow")
                            limpar_tela()
                            sleep(1.5)
                            continue
                        while ver_tit.verificar_titulo_de_eleitor_banco(novo_titulo) == (1,):
                            limpar_tela()
                            novo_titulo = ge.input_cancelavel("Título já cadastrado. Digite novamente", "EDITAR TÍTULO")
                            if novo_titulo is None:
                                limpar_tela()
                                break
                        if novo_titulo is None:
                            limpar_tela()
                            continue
                        editado = 1
                        cursor.execute('''
                        UPDATE eleitores SET titulo_eleitor = %s WHERE id = %s
                        ''', (novo_titulo, id_eleitor))
                        conexao.commit()
                        console.print("Título Editado Com Sucesso!", style="bold green")
                        limpar_tela()
                    case 3:
                        limpar_tela()
                        novo_cpf = ge.input_cancelavel("Novo CPF", "EDITAR CPF")
                        if novo_cpf is None:
                            limpar_tela()
                            continue
                        while not val_cpf.validacao_de_cpf(novo_cpf):
                            novo_cpf = ge.input_cancelavel("CPF inválido. Digite novamente", "EDITAR CPF")
                            if novo_cpf is None:
                                limpar_tela()
                                break
                        if novo_cpf is None:
                            limpar_tela()
                            continue
                        novo_cpf_criptografado = crip.criptografar_cpf(novo_cpf)
                        if novo_cpf_criptografado == eleitor['cpf']:
                            limpar_tela()
                            console.print("CPF igual ao atual. Nenhuma alteração feita.", style="bold yellow")
                            limpar_tela()
                            sleep(1.5)
                            continue
                        while ver_cpf.verificar_cpf_banco(novo_cpf_criptografado) == (1,):
                            novo_cpf = ge.input_cancelavel("CPF já cadastrado. Digite novamente", "EDITAR CPF")
                            if novo_cpf is None:
                                limpar_tela()
                                break
                            novo_cpf_criptografado = crip.criptografar_cpf(novo_cpf)
                        if novo_cpf is None:
                            limpar_tela()
                            continue

                        editado = 1
                        cursor.execute('''
                        UPDATE eleitores SET cpf = %s WHERE id = %s
                        ''', (novo_cpf_criptografado, id_eleitor))
                        conexao.commit()
                        console.print("CPF Editado Com Sucesso!", style="bold green")
                        limpar_tela()
                    case 4:
                        limpar_tela()
                        novo_mesario = ge.input_cancelavel('\nMesário: \n 1 - SIM \n 2 - NÃO')

                        if novo_mesario is None:
                            limpar_tela()
                            continue

                        elif novo_mesario == 2:
                            novo_mesario = 0
                            limpar_tela()

                        editado = 1
                        cursor.execute('''
                        UPDATE eleitores SET mesario = %s WHERE id = %s
                        ''', (novo_mesario, id_eleitor))
                        conexao.commit()
                        console.print("Mesário Editado Com Sucesso!", style="bold green")
                        limpar_tela()
                    case 5:
                        limpar_tela()
                        if editado == 1:
                            cursor.execute('SELECT * FROM eleitores WHERE id = %s', (id_eleitor,))
                            eleitor = cursor.fetchone()
                            exibir_tabela_eleitor("Eleitor Após Edição", eleitor)
                        else:
                            carregar_pontos_loop(3, "Encerrando Operação...")
                    case False:
                        break

            cursor.close()
            conexao.close()
            return confirmacao.confirmacao()
        case 2:
            return confirmacao.confirmacao()
    return None
