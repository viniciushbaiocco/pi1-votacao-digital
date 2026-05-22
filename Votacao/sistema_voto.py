from database import conexao_banco as conect
from Ocorrencias import voto_computado
from Ocorrencias import voto_duplo, geral
from Validadores import gerenciador_de_entrada as ge, validacao_voto as val_voto
from criptografia import criptografia as crip
from Verificadores import verificacao_cpf_votacao as ver_cpf_vot
from Verificadores import verificacao_eleitor_voto as ver_eleit_vot
from Verificadores import verificacao_chave_acesso_banco as ver_chave
from Validadores import validacao_cpf_votacao as val_cpf_vot, validacao_chave_acesso as val_chave, confirmacao
from Validadores import validacao_titulo as val_tit
from Verificadores import verificacao_titulo_banco as ver_tit
from Votacao import protocolo_votacao as prot_vot
from datetime import datetime
from Visual.visual import limpar_tela
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box

console = Console(highlight=False)

def exibir_progresso_votacao(cpf_4=None, titulo=None, chave=None):
    """
    Gera e renderiza uma tabela dinâmica com o progresso de identificação do eleitor.

    Esta função cria uma tabela centralizada via biblioteca Rich que serve como
    um painel de progresso visual para o eleitor. Conforme cada etapa da identificação
    é preenchida com sucesso (Fragmento do CPF, Título e Chave), os placeholders
    de interrogação ('?') são atualizados sequencialmente por textos verdes de confirmação.

    Args:
        cpf_4 (str, optional): Os 4 primeiros dígitos do CPF do eleitor. Padrão é None.
        titulo (str, optional): O título de eleitor informado. Padrão é None.
        chave (str, optional): A chave de acesso pessoal tratada do eleitor. Padrão é None.

    Returns:
        None: A função realiza apenas a renderização do componente visual na CLI.
    """
    tabela = Table(
        title="Identificação do Eleitor",
        box=box.DOUBLE,
        border_style="bold dodger_blue1",
        title_style="bold bright_white",
        header_style="bold dodger_blue1",
        show_lines=True
    )
    tabela.add_column("Campo", style="bright_white", min_width=22)
    tabela.add_column("Valor", min_width=30)

    tabela.add_row("CPF (4 primeiros dígitos)", f"[dim green]{cpf_4}[/dim green]" if cpf_4 is not None else "[dim]─[/dim]")
    tabela.add_row("Título de Eleitor", f"[dim green]{titulo}[/dim green]" if titulo is not None else "[dim]─[/dim]")
    tabela.add_row("Chave de Acesso", f"[dim green]Confirmada[/dim green]" if chave is not None else "[dim]─[/dim]")

    console.print(Align.center(tabela))

def exibir_candidato(candidato):
    conteudo = (
        f"[bright_white]Nome:[/bright_white]{candidato['nome']}\n"
        f"[bright_white]Partido:[/bright_white]{candidato['partido']}\n"
        f"[bright_white]Número Eleitoral:[/bright_white]{candidato['numero_votacao']}"
    )
    console.print(Panel(conteudo, title="[bold bright_white]CANDIDATO[/bold bright_white]", border_style="bold chartreuse1", box=box.DOUBLE, padding=(1, 2)))

def sistema_voto(id_sessao):
    """
    Gerencia a interface interativa, autenticação de eleitores e computação do voto.

    Esta é a função central do fluxo de votação em tempo real da urna eletrônica.
    A rotina é executada sob as seguintes diretrizes rígidas de segurança:

    1.  Fase de Autenticação: Solicita de maneira incremental os dados do eleitor (CPF,
        Título e Chave). Todos os inputs passam por validação de formato e, se cancelados
        pelo usuário, fecham o banco de dados e interrompem o fluxo com segurança.
    2.  Validação Criptográfica e Segurança Antifraude: Transforma os dados locais em hashes,
        valida o cadastro do cidadão no banco e checa se ele já votou (`ver_votou == (0,)`).
        Caso seja detectada uma tentativa de voto duplo, bloqueia a operação e grava alertas
        imediatos nos arquivos de auditoria.
    3.  Escolha do Candidato: Captura o número digitado. Se não existir, oferece um fluxo de
        contingência para confirmação de voto nulo (atribuindo ID '00'). Se existir, exibe o
        painel do candidato para revisão visual e confirmação de intenção do eleitor.

    4.  Gravação e Anonimato: Gera um protocolo de auditoria alfanumérico único desvinculado de
        dados pessoais, criptografa o protocolo, insere o registro na tabela de `votos` com a
        estampa de tempo truncada e atualiza o estado do eleitor para `status_votacao = 1` sob
        uma transação atômica (`commit`).

    Args:
        id_sessao (str ou int): O identificador exclusivo da sessão eleitoral ativa
        para fins de amarração técnica nos logs de auditoria de votos.

    Returns:
        None: A função gerencia entradas de usuários, mutações complexas de estados em banco
        de dados e gravações de arquivos de log, encerrando os fluxos por retornos antecipados.
    """
    limpar_tela()

    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    exibir_progresso_votacao()
    cpf_4 = ge.input_cancelavel("Digite os 4 primeiros dígitos do seu CPF", "IDENTIFICAÇÃO")
    if cpf_4 is None:
        cursor.close();
        conexao.close(); 
        return

    cpf_4_valido = val_cpf_vot.validar_cpf_voto(cpf_4)
    while cpf_4_valido == False:
        limpar_tela()
        exibir_progresso_votacao()
        cpf_4 = ge.input_cancelavel("CPF inválido. Digite novamente", "IDENTIFICAÇÃO")
        if cpf_4 is None:
            break
        cpf_4_valido = val_cpf_vot.validar_cpf_voto(cpf_4)
    if cpf_4 is None:
        cursor.close();
        conexao.close();
        return

    limpar_tela()
    exibir_progresso_votacao(cpf_4=cpf_4)
    titulo = ge.input_cancelavel("Digite seu Título de Eleitor", "IDENTIFICAÇÃO")
    if titulo is None:
        cursor.close();
        conexao.close();
        return

    titulo = titulo.strip()
    titulo_valido = val_tit.validar_titulo(titulo)
    while titulo_valido == False:
        limpar_tela()
        exibir_progresso_votacao(cpf_4=cpf_4)
        titulo = ge.input_cancelavel("Título inválido. Digite novamente", "IDENTIFICAÇÃO")
        if titulo is None:
            break
        titulo = titulo.strip()
        titulo_valido = val_tit.validar_titulo(titulo)
    if titulo is None:
        cursor.close();
        conexao.close();
        return

    limpar_tela()
    exibir_progresso_votacao(cpf_4=cpf_4, titulo=titulo)
    chave_acesso = ge.input_cancelavel("Digite sua Chave de Acesso", "IDENTIFICAÇÃO")
    if chave_acesso is None:
        cursor.close();
        conexao.close();
        return
    chave_acesso = chave_acesso.strip().upper()

    chave_valida = val_chave.validar_chave_acesso(chave_acesso)
    while chave_valida == False:
        limpar_tela()
        exibir_progresso_votacao(cpf_4=cpf_4, titulo=titulo)
        chave_acesso = ge.input_cancelavel("Chave inválida. Digite novamente", "IDENTIFICAÇÃO")
        if chave_acesso is None:
            break
        chave_acesso = chave_acesso.strip().upper()
        chave_valida = val_chave.validar_chave_acesso(chave_acesso)
    if chave_acesso is None:
        cursor.close();
        conexao.close();
        return

    limpar_tela()
    exibir_progresso_votacao(cpf_4=cpf_4, titulo=titulo, chave=chave_acesso)

    cpf_4= crip.criptografar_cpf(cpf_4)
    chave_acesso= crip.criptografar_chave_acesso(chave_acesso)
    ver_votou= ver_eleit_vot.verificacao_eleitor_voto(chave_acesso)
    votou  = 0
    opcao  = 2

    while opcao == 2:
        if ver_cpf_vot.verificar_cpf_voto(cpf_4) == (1,) and ver_chave.verificar_chave_acesso_banco(chave_acesso) == (1,) and ver_tit.verificar_titulo_de_eleitor_banco(titulo) == (1,):
            if ver_votou == (0,):
                voto = val_voto.validacao_voto()

                query = "SELECT COUNT(*) FROM candidatos WHERE numero_votacao = %s"
                cursor.execute(query, (voto,))
                resultado = cursor.fetchone()

                if resultado == {'COUNT(*)': 0}:
                    console.print("\n[bold yellow]Número não cadastrado. Se confirmar, o voto será considerado nulo.[/bold yellow]")
                    voto_nulo_opcao = ge.obter_entrada_inteira_valida('\n1 - Confirmar voto nulo \n2 - Tentar novamente \nDigite uma opção: ', 1, 2)
                    match voto_nulo_opcao:
                        case 1:
                            voto = 0
                            votou = 1
                            console.print('\n[bold green]Voto Computado![/bold green]')
                            cursor.execute('SELECT * FROM candidatos WHERE numero_votacao = %s', (voto,))
                            candidato = cursor.fetchone()
                            id_candidato = candidato['id']
                            opcao = 1
                        case 2:
                            pass
                else:
                    cursor.execute('SELECT * FROM candidatos WHERE numero_votacao = %s', (voto,))
                    candidato = cursor.fetchone()
                    id_candidato = candidato['id']
                    exibir_candidato(candidato)
                    opcao = ge.obter_entrada_inteira_valida('\nCerteza que deseja votar nesse candidato? \n1 - Sim \n2 - Não \nDigite uma opção: ', 1, 2)
                    match opcao:
                        case 1:
                            console.print('\n[bold green]Voto Computado![/bold green]')
                            votou = 1
                            opcao = 1
                        case 2:
                            pass

                if resultado == {'COUNT(*)': 0}:
                    voto = val_voto.validacao_voto()
                    query = "SELECT COUNT(*) FROM candidatos WHERE numero_votacao = %s"
                    cursor.execute(query, (voto,))
                    resultado = cursor.fetchone()

                    if resultado == {'COUNT(*)': 0}:
                        console.print('\n[bold yellow]Você digitou um candidato inexistente novamente, o voto será considerado nulo.[/bold yellow]')
                        votou = 1
                        voto  = 0
                        opcao = 1
                        cursor.execute('SELECT * FROM candidatos WHERE numero_votacao = %s', (voto,))
                        candidato = cursor.fetchone()
                        id_candidato = candidato['id']
                        console.print('\n[bold green]Voto Computado![/bold green]')
                    else:
                        cursor.execute('SELECT * FROM candidatos WHERE numero_votacao = %s', (voto,))
                        candidato = cursor.fetchone()
                        id_candidato = candidato['id']
                        exibir_candidato(candidato)
                        opcao = ge.obter_entrada_inteira_valida('\nCerteza que deseja votar nesse candidato? \n 1 - Sim \n 2 - Não \nDigite uma opção: ', 1, 2)
                        match opcao:
                            case 1:
                                console.print('\n[bold green]Voto Computado![/bold green]')
                                votou = 1
                                opcao = 1
                            case 2:
                                pass
            else:
                console.print('\n[bold red]Erro, tentativa de voto duplo.[/bold red]')
                voto_duplo.ocorrencia_voto_duplo(id_sessao)
                geral.ocorrencia_voto_duplo(id_sessao)
                confirmacao.confirmacao()
                opcao = 1

            if votou == 1:
                protocolo = prot_vot.gerar_protocolo_votacao(voto)
                console.print(f"\n[bold bright_white]Seu protocolo de votação é: {protocolo}[/bold bright_white]")
                confirmacao.confirmacao()
                protocolo= crip.criptografar_protocolo(protocolo)
                voto_computado.ocorrencia_voto_computado(id_sessao)
                geral.ocorrencia_voto_computado(id_sessao)
                data_hora= datetime.now()
                sem_milissegundosssegundos= data_hora.replace(microsecond=0)

                query_voto = 'INSERT INTO votos (id_candidato, data_hora, protocolo_votacao) VALUES (%s, %s, %s)'
                cursor.execute(query_voto, (id_candidato, sem_milissegundosssegundos, protocolo))

                query = 'UPDATE eleitores SET status_votacao = %s WHERE chave_acesso = %s'
                cursor.execute(query, (votou, chave_acesso))

                conexao.commit()
        else:
            console.print('\n[bold red]Erro ao verificar CPF ou chave de acesso do eleitor.[/bold red]')
            opcao = 1
            confirmacao.confirmacao()

    cursor.close()
    conexao.close()
