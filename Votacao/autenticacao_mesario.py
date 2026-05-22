from Validadores import gerenciador_de_entrada as ge, validacao_titulo as val_tit
from Validadores import validacao_cpf_votacao as val_cpf_vot
from Validadores import validacao_chave_acesso as val_chave
from Validadores import confirmacao
from Verificadores import verificacao_mesario_banco as ver_mes
from Ocorrencias import acesso_negado, geral
from criptografia import criptografia as crip
from database import conexao_banco as cb
from Gerenciamento import recuperacao_chave
from Visual.visual import limpar_tela
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box

console = Console(highlight=False)

def exibir_progresso_mesario(titulo=None, cpf_4=None, chave=None, tentativa=1):
    """
    Gera e renderiza uma tabela dinâmica com o progresso de validação do mesário.

    Esta função atua como um formulário visual incremental no terminal. Conforme o
    mesário preenche e valida cada dado (Título, fatiamento inicial do CPF e confirmação
    de Chave de Acesso), a tabela substitui os placeholders de interrogação ('?') por
    textos coloridos de confirmação. Exibe também o número da tentativa atual no cabeçalho.

    Args:
        titulo (str, optional): Título de eleitor informado e validado. Padrão é None.
        cpf_4 (str, optional): Os 4 primeiros dígitos do CPF informados. Padrão é None.
        chave (str, optional): Chave de acesso criptografada correspondente. Padrão é None.
        tentativa (int): O índice da tentativa atual do mesário (de 1 a 3). Padrão é 1.

    Returns:
        None: A função realiza apenas a exibição gráfica da tabela centralizada no terminal.
    """
    tabela = Table(
        title=f"Identificação do Mesário — Tentativa {tentativa} de 3",
        box=box.DOUBLE,
        border_style="bold chartreuse1",
        title_style="bold bright_white",
        header_style="bold chartreuse1",
        show_lines=True
    )
    tabela.add_column("Campo", style="bright_white", min_width=22)
    tabela.add_column("Valor", min_width=30)

    tabela.add_row("Título de Eleitor", f"[dim green]{titulo}[/dim green]" if titulo is not None else "[dim]─[/dim]")
    tabela.add_row("CPF (4 primeiros dígitos)", f"[dim green]{cpf_4}[/dim green]" if cpf_4 is not None else "[dim]─[/dim]")
    tabela.add_row("Chave de Acesso", f"[dim green]Confirmada[/dim green]" if chave is not None else "[dim]─[/dim]")

    console.print(Align.center(tabela))

def autenticar_mesario(id_sessao):
    """
    Executa o protocolo de autenticação multifator com limite de tentativas para mesários.

    A função restringe o acesso à urna por meio de um loop de até 3 tentativas.
    Para obter sucesso, o usuário deve passar por três barreiras de checagem:

    1.  Validar a sintaxe e a existência do Título de Eleitor associado a um perfil
        de mesário ativo no banco de dados (`mesario = 1`).
    2.  Validar se os 4 dígitos iniciais informados do CPF batem com o fragmento inicial
        da hash de CPF salva em banco.
    3.  Validar a assinatura criptográfica da Chave de Acesso.

    Caso ocorra erro em qualquer etapa da checagem, a conexão com o banco é encerrada com
    segurança, as tentativas restantes são calculadas e são gerados alertas em tempo real
    nos logs de auditoria local e geral. Na terceira falha consecutiva, o sistema bloqueia
    o acesso e oferece um atalho para invocar a rotina de recuperação de chave de backup.

    Args:
        id_sessao (str ou int): O identificador exclusivo da sessão ativa da urna eleitoral
        para fins de amarração de logs de auditoria.

    Returns:
        bool: True se o mesário passou com sucesso por todas as etapas de validação e
        criptografia; False se o processo foi cancelado voluntariamente ou se o número
        máximo de tentativas falhas foi atingido.
    """

    for tentativa in range(1, 4):
        limpar_tela()

        exibir_progresso_mesario(tentativa=tentativa)
        titulo = ge.input_cancelavel("Digite seu Título de Eleitor", "IDENTIFICAÇÃO DO MESÁRIO")
        if titulo is None:
            return False

        titulo = titulo.strip()
        titulo_valido = val_tit.validar_titulo(titulo)
        while not titulo_valido:
            limpar_tela()
            exibir_progresso_mesario(tentativa=tentativa)
            titulo = ge.input_cancelavel("Título inválido. Digite novamente", "IDENTIFICAÇÃO DO MESÁRIO")
            if titulo is None:
                return False
            titulo = titulo.strip()
            titulo_valido = val_tit.validar_titulo(titulo)

        conexao = cb.conexao_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(*) FROM eleitores WHERE titulo_eleitor = %s AND mesario = 1", (titulo,))
        if cursor.fetchone() == (0,):
            cursor.close(); conexao.close()
            limpar_tela()
            exibir_progresso_mesario(tentativa=tentativa)
            console.print("\n[bold red]Acesso negado. Eleitor não possui perfil de mesário.[/bold red]")
            if tentativa < 3:
                console.print(f"[dim]Tentativas restantes: {3 - tentativa}[/dim]")
            confirmacao.confirmacao()
            geral.ocorrencia_acesso_negado(id_sessao)
            acesso_negado.ocorrencia_acesso_negado(id_sessao)
            continue
        cursor.close(); conexao.close()

        limpar_tela()
        exibir_progresso_mesario(titulo=titulo, tentativa=tentativa)
        cpf_4 = ge.input_cancelavel("Digite os 4 primeiros dígitos do seu CPF", "IDENTIFICAÇÃO DO MESÁRIO")
        if cpf_4 is None:
            return False

        cpf_4_valido = val_cpf_vot.validar_cpf_voto(cpf_4)
        while not cpf_4_valido:
            limpar_tela()
            exibir_progresso_mesario(titulo=titulo, tentativa=tentativa)
            cpf_4 = ge.input_cancelavel("CPF inválido. Digite novamente", "IDENTIFICAÇÃO DO MESÁRIO")
            if cpf_4 is None:
                return False
            cpf_4_valido = val_cpf_vot.validar_cpf_voto(cpf_4)

        cpf_4_criptografado = crip.criptografar_cpf(cpf_4)
        conexao = cb.conexao_banco()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM eleitores WHERE titulo_eleitor = %s AND SUBSTRING(cpf, 1, 4) = %s AND mesario = 1",
            (titulo, cpf_4_criptografado[:4])
        )
        if cursor.fetchone() == (0,):
            cursor.close(); conexao.close()
            limpar_tela()
            exibir_progresso_mesario(titulo=titulo, tentativa=tentativa)
            console.print("\n[bold red]Os primeiros 4 dígitos do CPF não correspondem. Acesso negado.[/bold red]")
            if tentativa < 3:
                console.print(f"[dim]Tentativas restantes: {3 - tentativa}[/dim]")
            confirmacao.confirmacao()
            geral.ocorrencia_acesso_negado(id_sessao)
            acesso_negado.ocorrencia_acesso_negado(id_sessao)
            continue
        cursor.close(); conexao.close()

        limpar_tela()
        exibir_progresso_mesario(titulo=titulo, cpf_4=cpf_4, tentativa=tentativa)
        chave_acesso = ge.input_cancelavel("Digite sua Chave de Acesso", "IDENTIFICAÇÃO DO MESÁRIO")
        if chave_acesso is None:
            return False
        chave_acesso = chave_acesso.strip().upper()

        chave_valida = val_chave.validar_chave_acesso(chave_acesso)
        while not chave_valida:
            limpar_tela()
            exibir_progresso_mesario(titulo=titulo, cpf_4=cpf_4, tentativa=tentativa)
            chave_acesso = ge.input_cancelavel("Chave inválida. Digite novamente", "IDENTIFICAÇÃO DO MESÁRIO")
            if chave_acesso is None:
                return False
            chave_acesso = chave_acesso.strip().upper()
            chave_valida = val_chave.validar_chave_acesso(chave_acesso)

        chave_acesso_criptografada = crip.criptografar_chave_acesso(chave_acesso)
        resultado = ver_mes.verificar_mesario(titulo, cpf_4_criptografado, chave_acesso_criptografada)

        if resultado == (1,):
            limpar_tela()
            exibir_progresso_mesario(titulo=titulo, cpf_4=cpf_4, chave=chave_acesso, tentativa=tentativa)
            console.print("\n[bold green]Mesário validado com sucesso![/bold green]")
            input("\nPressione Enter para continuar...")
            return True

        limpar_tela()
        exibir_progresso_mesario(titulo=titulo, cpf_4=cpf_4, tentativa=tentativa)
        console.print("\n[bold red]Chave de acesso inválida. Acesso negado.[/bold red]")

        if tentativa < 3:
            console.print(f"[dim]Tentativas restantes: {3 - tentativa}[/dim]")
            titulo_painel = "[bold bright_white]RECUPERAR CHAVE DE ACESSO?[/bold bright_white]"
            borda_painel = "bold sandy_brown"
            aviso = ""
        else:
            titulo_painel = "[bold red]ÚLTIMA TENTATIVA ESGOTADA[/bold red]"
            borda_painel = "bold red"
            aviso = "[bold red]Esta foi sua última tentativa.[/bold red] O acesso está bloqueado.\nRecupere sua chave para tentar novamente na próxima sessão.\n\n"

        console.print(Panel(
            Align.center(f"{aviso}[bold bright_white][1][/bold bright_white]  Sim\n[dim]──────────────────────────────[/dim]\n[dim red][X]  Não[/dim red]"),
            title=titulo_painel,
            border_style=borda_painel,
            box=box.DOUBLE,
            padding=(1, 4)
        ))
        opcao = ge.obter_entrada_inteira_valida("Escolha: ", 1, 1)
        if opcao == 1:
            recuperacao_chave.recuperar_chave()
        else:
            confirmacao.confirmacao()
        geral.ocorrencia_acesso_negado(id_sessao)
        acesso_negado.ocorrencia_acesso_negado(id_sessao)

    limpar_tela()
    console.print("\n[bold red]Número máximo de tentativas atingido. Acesso bloqueado.[/bold red]")
    confirmacao.confirmacao()
    return False
