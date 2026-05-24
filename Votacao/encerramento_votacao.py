from Verificadores import verificacao_chave_acesso_banco
from Validadores import validacao_chave_acesso, confirmacao
from Validadores import gerenciador_de_entrada as ge
from database import conexao_banco
from Votacao import autenticacao_mesario
from Gerenciamento import recuperacao_chave
from criptografia import criptografia as cripto
from Ocorrencias import encerramento_urna, geral
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich import box
from Visual.visual import limpar_tela

console = Console(highlight=False)

def encerrar_sistema_votacao(id_sessao):
    """
    Executa o protocolo de segurança para o encerramento oficial da sessão de votação.

    A função atua em camadas sucessivas de validação para impedir o fechamento acidental
    ou não autorizado da urna eletrônica:

    1.  Invoca o módulo de autenticação multifator para validar a identidade e o perfil do mesário.
    2.  Solicita uma confirmação explícita de intenção de encerramento por parte do usuário.
    3.  Exige um segundo desafio de segurança, forçando o mesário a digitar sua chave de acesso
        pessoal sob um limite estrito de até 3 tentativas, protegendo o estado contra força bruta.

    Se o desafio for superado, a função consolida o encerramento e dispara a gravação dos logs
    físicos de auditoria local e geral. Caso ocorra qualquer erro sistêmico no processo, um
    mecanismo de `rollback` é acionado preventivamente. O fechamento dos cursores e conexões
    é garantido no bloco `finally`.

    Args:
        id_sessao (int ou str): O identificador exclusivo da sessão de urna ativa
        que está sendo finalizada.

    Returns:
        bool: True se o protocolo de encerramento e escrita de logs foi concluído com
        sucesso; False se o mesário falhou nas autenticações, cancelou a operação ou se
        ocorreu uma exceção de banco de dados.
    """

    limpar_tela()

    if not autenticacao_mesario.autenticar_mesario(id_sessao):
        return False

    conexao = conexao_banco.conexao_banco()

    try:

        limpar_tela()

        resposta = ge.input_cancelavel("Deseja realmente encerrar o sistema de votação? "
                                       "\n[bold white][1][/bold white] Sim", "Encerrar Sistema")

        if not resposta:
            limpar_tela()
            console.print("\nEncerramento cancelado.", style="bold yellow")
            confirmacao.confirmacao()
            return False

        chave_confirmada = False
        for tentativa in range(1, 4):
            limpar_tela()
            confirmacao_chave = ge.input_cancelavel("Confirme sua chave de acesso pessoal", "CONFIRMAÇÃO DE ENCERRAMENTO")
            if confirmacao_chave is None:
                return False
            confirmacao_chave = validacao_chave_acesso.remover_acentos(confirmacao_chave.strip()).upper()

            if not validacao_chave_acesso.validar_chave_acesso(confirmacao_chave):
                limpar_tela()
                console.print("\n[bold red]Chave inválida. Tente novamente.[/bold red]")
                confirmacao.confirmacao()
                continue

            confirmacao_chave_criptografada = cripto.criptografar_chave_acesso(confirmacao_chave)
            if verificacao_chave_acesso_banco.verificar_chave_acesso_banco(confirmacao_chave_criptografada) != (0,):
                chave_confirmada = True
                break

            limpar_tela()
            console.print("\n[bold red]Chave de acesso não confere. Acesso negado.[/bold red]")
            if tentativa < 3:
                limpar_tela()
                console.print(f"[dim]Tentativas restantes: {3 - tentativa}[/dim]")
                titulo_painel = "[bold bright_white]RECUPERAR CHAVE DE ACESSO?[/bold bright_white]"
                borda_painel = "bold sandy_brown"
                aviso = ""
            else:
                limpar_tela()
                titulo_painel = "[bold red]ÚLTIMA TENTATIVA ESGOTADA[/bold red]"
                borda_painel = "bold red"
                aviso = "[bold red]Esta foi sua última tentativa.[/bold red] O encerramento está bloqueado.\nRecupere sua chave para tentar novamente na próxima sessão.\n\n"

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

        if not chave_confirmada:
            limpar_tela()
            console.print("\n[bold red]Encerramento cancelado. Número máximo de tentativas atingido.[/bold red]")
            confirmacao.confirmacao()
            return False

        limpar_tela()
        console.print("\nSistema de votação encerrado.", style="bold green")

        encerramento_urna.ocorrencia_encerramento_urna(id_sessao)
        geral.ocorrencia_encerramento_urna(id_sessao)
        confirmacao.confirmacao()

        return True

    except Exception:
        limpar_tela()
        console.print("\nErro ao registrar encerramento.", style="bold red")
        if conexao:
            conexao.rollback()
        return False

    finally:
        if conexao:
            conexao.close()
