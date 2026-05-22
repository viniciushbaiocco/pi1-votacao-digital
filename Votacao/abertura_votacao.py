from Zerezima import zerezima
from Votacao import autenticacao_mesario
from Ocorrencias import abertura_urna, geral
from Visual.visual import limpar_tela
from database import conexao_banco
from Validadores import confirmacao
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich import box

console = Console(highlight=False)

def verificar_candidatos():
    """
    Valida o quantitativo de candidatos reais e garante a existência do registro de voto nulo.

    Esta função realiza duas checagens na tabela de candidatos:
    1. Conta quantos candidatos válidos estão registrados (cujo número de votação é diferente de '00').
    2. Verifica a existência do registro estrutural do 'Voto Nulo' (número '00'). Caso este registro
        não seja localizado na base de dados, a função realiza uma inserção automática (INSERT)
        e um commit para garantir que o sistema consiga computar votos nulos corretamente.

    Args:
        None.

    Returns:
        int: O volume total de candidatos reais cadastrados no sistema (desconsiderando o voto nulo).
    """
    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM candidatos WHERE numero_votacao != '00'")
    total_candidatos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM candidatos WHERE numero_votacao = '00'")
    voto_nulo_existe = cursor.fetchone()[0]

    if voto_nulo_existe == 0:
        cursor.execute(
            "INSERT INTO candidatos (nome, partido, sigla_partido, numero_votacao) VALUES (%s, %s, %s, %s)",
            ('Voto Nulo', 'Nulo', 'NULO', '00')
        )
        conexao.commit()

    cursor.close()
    conexao.close()

    return total_candidatos

def abrir_sistema_votacao(id_sessao):
    """
    Gerencia as etapas de segurança e autorização necessárias para abrir o terminal de votação.

    A função executa o fluxo rígido de preparação da urna eletrônica através dos seguintes passos:

    1.  Solicita e valida as credenciais do mesário. Caso falhe, aborta o processo imediatamente.
    2.  Consulta o banco para verificar se existem candidatos reais cadastrados. Se a contagem for
        igual a zero, a abertura é negada através de um painel informativo via Rich.
    3.  Caso o mesário seja válido e haja candidatos, dispara o procedimento de auditoria da Zerésima.
    4.  Grava os arquivos de log locais e gerais de auditoria notificando o início bem-sucedido.

    Args:
        id_sessao (str ou int): O identificador exclusivo da sessão eleitoral que está sendo iniciada.

    Returns:
        bool: True se o sistema de votação foi aberto com sucesso após todas as validações de
        segurança e regras de negócio; False caso contrário.
    """
    limpar_tela()
    if not autenticacao_mesario.autenticar_mesario(id_sessao):
        console.print("\n[bold red][ERRO] Validação falhou.[/bold red]")
        console.print("[bold yellow]Confirme se o eleitor possui perfil de mesário.[/bold yellow]")
        return False

    total_candidatos = verificar_candidatos()

    if total_candidatos == 0:
        console.print(Panel(
            Align.center("[bold red]Nenhum candidato cadastrado no sistema.[/bold red]\n"
                         "[bold yellow]Cadastre ao menos um candidato antes de abrir a votação.[/bold yellow]"),
            title="[bold bright_white]ABERTURA NEGADA[/bold bright_white]",
            border_style="bold red",
            box=box.DOUBLE,
            padding=(1, 4)
        ))
        confirmacao.confirmacao()
        return False

    zerezima.zerezima()
    geral.ocorrencia_abertura_urna(id_sessao)
    abertura_urna.ocorrencia_abertura_urna(id_sessao)
    return True
