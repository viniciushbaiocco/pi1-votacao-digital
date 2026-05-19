from database import conexao_banco as cb
from Visual.visual import limpar_tela
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich import box

console = Console(highlight=False)

def zerezima():
      limpar_tela()

      conexao = cb.conexao_banco()
      cursor = conexao.cursor()

      console.print("\n[bold bright_white]Iniciando zerézima...[/bold bright_white]")

      truncar_votos = "TRUNCATE votos;"
      cursor.execute(truncar_votos)
      conexao.commit()
      console.print("[bold yellow]Eliminando todos os votos registrados na tabela 'Votos'...[/bold yellow]")

      resetar_status_eleitores = "UPDATE eleitores SET status_votacao = 0;"
      cursor.execute(resetar_status_eleitores)
      conexao.commit()
      console.print("[bold yellow]Atualizando status de votação de eleitores para 'Não'...[/bold yellow]")

      console.print("\n[bold green]Zerézima finalizada![/bold green]\n")

      buscar_candidatos = "SELECT candidatos.nome, candidatos.sigla_partido, COUNT(votos.id) AS total_votos FROM candidatos LEFT JOIN votos ON candidatos.id = votos.id_candidato GROUP BY candidatos.id;"
      cursor.execute(buscar_candidatos)
      candidatos = cursor.fetchall()

      tabela = Table(
            title="Candidatos — Votos Zerados",
            box=box.DOUBLE,
            border_style="bold chartreuse1",
            title_style="bold bright_white",
            header_style="bold chartreuse1",
            show_lines=True
      )
      tabela.add_column("Candidato", style="bright_white")
      tabela.add_column("Partido", style="bright_white", justify="center")
      tabela.add_column("Votos", style="bright_white", justify="center")

      for nome, partido, votos in candidatos:
            tabela.add_row(nome, partido, str(votos))

      console.print(Align.center(tabela))

      input("\nPressione Enter para continuar...")

      cursor.close()
      conexao.close()
