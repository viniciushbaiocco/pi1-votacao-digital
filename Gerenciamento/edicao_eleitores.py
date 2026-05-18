from database import conexao_banco as conect
from criptografia import criptografia as crip
from Verificadores import verificacao_cpf_banco as ver_cpf
from Verificadores import verificacao_titulo_banco as ver_tit
from Cadastro import chave_acesso as chave
from Validadores import confirmacao, gerenciador_de_entrada as ge, validacao_cpf as val_cpf, validacao_nome as val_nome, \
    validacao_titulo as val_tit
from rich.console import Console
from rich.table import Table
from rich import box
from Visual.visual import limpar_tela

console = Console(highlight=False)

def exibir_tabela_eleitor(titulo, eleitor):

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
    console.print(tabela)

def edicao_eleitores():
    """
    A função exibe opções para receber valores str de cpf ou titulo de eleitor para editar um eleitor.

    Args:
        None

    Returns:
        O eleitor editado
    """

    limpar_tela()

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    console.print("\n[bold bright_white]--- 2 - Edição de Eleitores ---[/bold bright_white]")
    console.print("\nOpção 1: Busca pelo CPF\nOpção 2: Busca pelo Título de Eleitor")
    opcao = ge.obter_entrada_inteira_valida('\nDigite uma opção: ', 1, 2)

    match opcao:
        case 1:
            cpf = input('\nCPF: ')
            while val_cpf.validacao_de_cpf(cpf) == False:
                cpf = input('\nCPF inválido, digite novamente: ')
            cursor.execute('SELECT id FROM eleitores WHERE cpf = %s', (crip.criptografar_cpf(cpf),))
            if ver_cpf.verificar_cpf_banco(crip.criptografar_cpf(cpf)) == (0,):
                console.print("\n*** Eleitor não cadastrado! *** \nRealizar o cadastramento no Menu Gerenciamento de Eleitores.", style="bold yellow")
        case 2:
            tit = input('\nTítulo de Eleitor: ')
            while val_tit.validar_titulo(tit) == False:
                tit = input('\nTítulo de Eleitor inválido, digite novamente: ')
            cursor.execute('SELECT id FROM eleitores WHERE titulo_eleitor = %s', (tit,))
            if ver_cpf.verificar_cpf_banco(tit) == (0,):
                console.print("\n*** Eleitor não cadastrado! *** \nRealizar o cadastramento no Menu Gerenciamento de Eleitores.", style="bold yellow")

    eleitor = cursor.fetchone()
    if eleitor is None:
        return confirmacao.confirmacao()
    id_eleitor = eleitor['id']

    cursor.execute('SELECT * FROM eleitores WHERE id = %s', (id_eleitor,))
    eleitor = cursor.fetchone()
    cpf_desc = crip.descriptografar_cpf(eleitor['cpf'])

    exibir_tabela_eleitor("Eleitor a Ser Editado", eleitor)

    console.print("\nDeseja realmente editar esse eleitor?\n1 - Sim\n2 - Não")
    opcao2 = ge.obter_entrada_inteira_valida('\nDigite uma opção: ', 1, 2)
    editado = 0
    match opcao2:
        case 1:
            opcao_editar = 0
            while opcao_editar != 5:
                print('\nO Que Deseja Editar \n[1] Nome \n[2] Título \n[3] CPF \n[4] Mesário \n[5] Confirmar')
                opcao_editar = ge.obter_entrada_inteira_valida('\nDigite uma opção: ',1, 5)
                match opcao_editar:
                    case 1:
                        novo_nome = val_nome.validar_nome()
                        nova_chave_acesso = chave.geracao_chave_acesso(novo_nome)

                        editado = 1
                        cursor.execute('''
                        UPDATE eleitores SET nome = %s, chave_acesso = %s
                                            WHERE id = %s
                        ''', (novo_nome, nova_chave_acesso, id_eleitor))
                        conexao.commit()

                        console.print(f'[bold bright_green]Nome Editado Com Sucesso![/bold bright_green]')
                        console.print(f'Sua Nova Chave de Acesso é: [bold bright_yellow]{nova_chave_acesso}[/bold bright_yellow]')
                    case 2:
                        novo_titulo = input('\nDigite o novo Título de Eleitor: ')
                        while val_tit.validar_titulo(novo_titulo) == False:
                            novo_titulo = input('\nNovo Título de Eleitor inválido, digite novamente: ')
                        while ver_tit.verificar_titulo_de_eleitor_banco(novo_titulo) == (1,):
                            novo_titulo = input('\nTítulo de Eleitor já cadastrado, digite novamente: ')
                        novo_titulo_verificado = novo_titulo
                        
                        editado = 1
                        cursor.execute('''
                        UPDATE eleitores SET
                                        titulo_eleitor = %s WHERE id = %s
                        ''', (novo_titulo_verificado, id_eleitor))
                        conexao.commit()

                        print('Título Editado Com Sucesso!')
                    case 3:
                        novo_cpf = input('\nDigite o novo CPF: ')
                        novo_cpf_criptografado = crip.criptografar_cpf(novo_cpf)
                        while val_cpf.validacao_de_cpf(novo_cpf) == False:
                            novo_cpf = input('\nNovo CPF inválido, digite novamente: ')
                        while ver_cpf.verificar_cpf_banco(novo_cpf_criptografado) == (1,):
                            novo_cpf = input('\nCPF já cadastrado, digite novamente: ')
                            novo_cpf_criptografado = crip.criptografar_cpf(novo_cpf)
                        
                        editado = 1
                        cursor.execute('''
                        UPDATE eleitores SET
                                        cpf = %s WHERE id = %s
                        ''', (novo_cpf_criptografado, id_eleitor))
                        conexao.commit()

                        print('CPF Editado Com Sucesso!')
                    case 4:
                        novo_mesario = ge.obter_entrada_inteira_valida('\nMesário: \n 1 - SIM \n 2 - NÃO \n Escolha: ', 1, 2)
                        if novo_mesario == 2:
                            novo_mesario = 0

                        editado = 1
                        cursor.execute('''
                        UPDATE eleitores SET
                                        mesario = %s WHERE id = %s
                        ''', (novo_mesario, id_eleitor))
                        conexao.commit()

                        print('Mesário Editado Com Sucesso!')
                    case 5:
                        if editado == 1:
                            cursor.execute('SELECT * FROM eleitores WHERE id = %s', (id_eleitor,))
                            eleitor = cursor.fetchone()

                            exibir_tabela_eleitor("Eleitor Após Edição", eleitor)
                        else:
                            print('Encerrando Operação...')

            cursor.close()
            conexao.close()
            return confirmacao.confirmacao()
        case 2:
            return confirmacao.confirmacao()
