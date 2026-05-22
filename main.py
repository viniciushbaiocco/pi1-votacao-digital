import os
from Menu import menu_completo
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich import box
from Visual.visual import limpar_tela

console = Console(highlight=False)

def exibir_splash():
    """
    Renderiza a tela de abertura (Splash Screen) responsiva do sistema eleitoral.

    A função projeta uma interface visual de apresentação na CLI antes de iniciar a
    aplicação. Ela mede dinamicamente o tamanho atual da janela do terminal utilizando
    `os.get_terminal_size().columns` para centralizar as linhas textuais de forma
    proporcional. Caso o ambiente não possua suporte a console físico (disparando um
    `OSError`), um fallback seguro de 80 colunas é aplicado.

    A identidade visual utiliza a biblioteca Pyfiglet para estilizar o nome "LAD.PY" em
    arte ASCII e aplica um degradê cíclico nas cores verde e amarela através do operador
    de módulo (`%`). Ao final, exibe um painel Rich descritivo com bordas duplas e suspende
    a execução do script aguardando uma interação de teclado (`input()`).

    Args:
        None.

    Returns:
        None: A função atua estritamente na leitura de metadados da janela e renderização
        de componentes gráficos na saída padrão (stdout).
    """
    limpar_tela()
    try:
        largura_terminal = os.get_terminal_size().columns
    except OSError:
        largura_terminal = 80

    arte = pyfiglet.figlet_format("LAD.PY", font="standard")
    cores_brasil = ["bold green", "bold green", "bold yellow", "bold yellow", "bold green", "bold green"]

    console.print("═" * largura_terminal, style="bold yellow")
    console.print()
    for i, linha in enumerate(arte.split('\n')):
        cor = cores_brasil[i % len(cores_brasil)]
        console.print(linha.center(largura_terminal), style=cor)
    console.print()
    console.print("Sistema de Votação Digital".center(largura_terminal), style="bright_white")
    console.print()
    console.print("═" * largura_terminal, style="bold yellow")
    console.print()

    descricao = (
        "[bright_white]Sistema eleitoral digital desenvolvido com segurança de ponta a ponta.[/bright_white]\n"
        "[dim]Garantindo integridade, rastreabilidade e confiabilidade em cada etapa da votação.[/dim]"
    )
    console.print(Panel(Align.center(descricao), border_style="bold spring_green1", box=box.DOUBLE, padding=(1, 4)))
    console.print()
    console.print("Pressione Enter para iniciar...".center(largura_terminal), style="dim")
    input()

if __name__ == "__main__":
    exibir_splash()
    menu_completo.menu_completo()