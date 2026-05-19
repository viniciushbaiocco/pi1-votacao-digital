from Zerezima import zerezima
from Votacao import autenticacao_mesario
from Ocorrencias import abertura_urna, geral
from Visual.visual import limpar_tela
from rich.console import Console

console = Console(highlight=False)

def abrir_sistema_votacao(id_sessao):
    limpar_tela()
    if not autenticacao_mesario.autenticar_mesario(id_sessao):
        console.print("\n[bold red][ERRO] Validação falhou.[/bold red]")
        console.print("[bold yellow]Confirme se o eleitor possui perfil de mesário.[/bold yellow]")
        return False

    zerezima.zerezima()
    geral.ocorrencia_abertura_urna(id_sessao)
    abertura_urna.ocorrencia_abertura_urna(id_sessao)
    return True
