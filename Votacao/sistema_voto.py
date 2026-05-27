from database import conexao_banco as conect
from Ocorrencias import voto_computado
from Ocorrencias import voto_duplo, geral, protocolo_votacao
from Validadores import gerenciador_de_entrada as ge, validacao_voto as val_voto
from criptografia import criptografia as crip
from Verificadores import verificacao_eleitor_voto as ver_eleit_vot
from Validadores import validacao_cpf_votacao as val_cpf_vot, validacao_chave_acesso as val_chave, confirmacao
from Validadores import validacao_titulo as val_tit
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

    tabela.add_row("CPF (4 primeiros dígitos)", f"[green]{cpf_4}[/green]" if cpf_4 is not None else "[dim]─[/dim]")
    tabela.add_row("Título de Eleitor", f"[green]{titulo}[/green]" if titulo is not None else "[dim]─[/dim]")
    tabela.add_row("Chave de Acesso", f"[green]Confirmada[/green]" if chave is not None else "[dim]─[/dim]")

    console.print(Align.center(tabela))

def exibir_candidato(candidato):
    """
    Renderiza um painel visual com os dados do candidato selecionado pelo eleitor.

    A função monta um painel centralizado via biblioteca Rich exibindo o nome, o
    partido e o número eleitoral do candidato. É utilizada na etapa de votação para
    que o eleitor revise e confirme visualmente a sua escolha antes de o voto ser
    efetivamente computado.

    Args:
        candidato (dict): Dicionário com os dados do candidato, contendo as chaves
        'nome', 'partido' e 'numero_votacao'.

    Returns:
        None: A função realiza apenas a renderização do componente visual na CLI.
    """
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
        valida a identidade do cidadão (título + CPF + chave na mesma consulta) e checa se já votou.
        Caso seja detectada uma tentativa de voto duplo, bloqueia a operação e grava alertas
        imediatos nos arquivos de auditoria.
    3.  Escolha do Candidato: Captura o número digitado. Se não existir, oferece um fluxo de
        contingência para confirmação de voto nulo (número '00'). Se existir, exibe o
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
        cursor.close()
        conexao.close()
        return

    cpf_4_valido = val_cpf_vot.validar_cpf_voto(cpf_4)
    while not cpf_4_valido:
        limpar_tela()
        exibir_progresso_votacao()
        cpf_4 = ge.input_cancelavel("CPF inválido. Digite novamente", "IDENTIFICAÇÃO")
        if cpf_4 is None:
            break
        cpf_4_valido = val_cpf_vot.validar_cpf_voto(cpf_4)
    if cpf_4 is None:
        cursor.close()
        conexao.close()
        return

    cpf_4 = cpf_4.replace(" ", "")

    limpar_tela()
    exibir_progresso_votacao(cpf_4=cpf_4)
    titulo = ge.input_cancelavel("Digite seu Título de Eleitor", "IDENTIFICAÇÃO")
    if titulo is None:
        cursor.close()
        conexao.close()
        return

    titulo = titulo.replace(" ", "")
    titulo_valido = val_tit.validar_titulo(titulo)
    while not titulo_valido:
        limpar_tela()
        exibir_progresso_votacao(cpf_4=cpf_4)
        titulo = ge.input_cancelavel("Título inválido. Digite novamente", "IDENTIFICAÇÃO")
        if titulo is None:
            break
        titulo = titulo.replace(" ", "")
        titulo_valido = val_tit.validar_titulo(titulo)
    if titulo is None:
        cursor.close()
        conexao.close()
        return

    limpar_tela()
    exibir_progresso_votacao(cpf_4=cpf_4, titulo=titulo)
    chave_acesso = ge.input_cancelavel("Digite sua Chave de Acesso", "IDENTIFICAÇÃO")
    if chave_acesso is None:
        cursor.close()
        conexao.close()
        return
    chave_acesso = val_chave.remover_acentos(chave_acesso.strip()).upper()

    chave_valida = val_chave.validar_chave_acesso(chave_acesso)
    while not chave_valida:
        limpar_tela()
        exibir_progresso_votacao(cpf_4=cpf_4, titulo=titulo)
        chave_acesso = ge.input_cancelavel("Chave inválida. Digite novamente", "IDENTIFICAÇÃO")
        if chave_acesso is None:
            break
        chave_acesso = val_chave.remover_acentos(chave_acesso.strip()).upper()
        chave_valida = val_chave.validar_chave_acesso(chave_acesso)
    if chave_acesso is None:
        cursor.close()
        conexao.close()
        return

    limpar_tela()
    exibir_progresso_votacao(cpf_4=cpf_4, titulo=titulo, chave=chave_acesso)

    cpf_4 = crip.criptografar_cpf(cpf_4)
    chave_acesso = crip.criptografar_chave_acesso(chave_acesso)

    if ver_eleit_vot.verificar_identidade_eleitor(titulo, cpf_4, chave_acesso)[0] == 0:
        limpar_tela()
        console.print('\n[bold red]Erro ao verificar CPF, título ou chave de acesso do eleitor.[/bold red]')
        confirmacao.confirmacao()
        cursor.close()
        conexao.close()
        return

    if ver_eleit_vot.verificacao_eleitor_voto(chave_acesso)[0] != 0:
        limpar_tela()
        console.print('\n[bold red]Erro, tentativa de voto duplo.[/bold red]')
        voto_duplo.ocorrencia_voto_duplo(id_sessao)
        geral.ocorrencia_voto_duplo(id_sessao)
        confirmacao.confirmacao()
        cursor.close()
        conexao.close()
        return

    votou = 0
    while not votou:
        voto = val_voto.validacao_voto()

        cursor.execute("SELECT COUNT(*) AS total FROM candidatos WHERE numero_votacao = %s", (voto,))
        candidato_existe = cursor.fetchone()['total'] > 0

        if not candidato_existe:
            limpar_tela()
            console.print("\n[bold yellow]Número não cadastrado. Se confirmar, o voto será considerado nulo.[/bold yellow]")
            escolha = ge.obter_entrada_inteira_valida('\n1 - Confirmar voto nulo \n2 - Tentar novamente \nDigite uma opção: ', 1, 2)
            if escolha == 1:
                voto = '00'
                votou = 1
            else:
                continue
        else:
            limpar_tela()
            cursor.execute('SELECT * FROM candidatos WHERE numero_votacao = %s', (voto,))
            candidato = cursor.fetchone()
            exibir_candidato(candidato)
            escolha = ge.obter_entrada_inteira_valida('\nCerteza que deseja votar nesse candidato? \n1 - Sim \n2 - Não \nDigite uma opção: ', 1, 2)
            if escolha != 1:
                continue
            votou = 1

    # Recupera o id do candidato escolhido (ou do registro de voto nulo '00')
    cursor.execute('SELECT id FROM candidatos WHERE numero_votacao = %s', (voto,))
    id_candidato = cursor.fetchone()['id']

    limpar_tela()
    console.print('\n[bold green]Voto Computado![/bold green]')

    # Protocolo único (coluna protocolo_votacao é UNIQUE): regenera em caso de colisão
    protocolo = prot_vot.gerar_protocolo_votacao(voto)
    protocolo_cripto = crip.criptografar_protocolo(protocolo)
    cursor.execute("SELECT COUNT(*) AS total FROM votos WHERE protocolo_votacao = %s", (protocolo_cripto,))
    while cursor.fetchone()['total'] > 0:
        protocolo = prot_vot.gerar_protocolo_votacao(voto)
        protocolo_cripto = crip.criptografar_protocolo(protocolo)
        cursor.execute("SELECT COUNT(*) AS total FROM votos WHERE protocolo_votacao = %s", (protocolo_cripto,))

    console.print(f"\n[bold bright_white]Seu protocolo de votação é: {protocolo}[/bold bright_white]")

    confirmacao.confirmacao()

    voto_computado.ocorrencia_voto_computado(id_sessao)
    protocolo_votacao.ocorrencia_protocolo_votacao(id_sessao)
    geral.ocorrencia_protocolo_votacao(id_sessao)
    geral.ocorrencia_voto_computado(id_sessao)

    data_hora = datetime.now()
    sem_milissegundos = data_hora.replace(microsecond=0)

    cursor.execute(
        'INSERT INTO votos (id_candidato, data_hora, protocolo_votacao) VALUES (%s, %s, %s)',
        (id_candidato, sem_milissegundos, protocolo_cripto)
    )
    cursor.execute(
        'UPDATE eleitores SET status_votacao = %s WHERE chave_acesso = %s',
        (1, chave_acesso)
    )
    conexao.commit()

    cursor.close()
    conexao.close()
