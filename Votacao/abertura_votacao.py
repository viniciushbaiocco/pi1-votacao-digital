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
