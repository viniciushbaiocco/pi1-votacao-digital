import time
from database import conexao_banco as cb
from Visual.visual import limpar_tela
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box

console = Console(highlight=False)

def zeresima():
      """
      Executa o procedimento de Zerésima para inicialização segura da urna eletrônica.

      Esta função realiza a auditoria e o reset completo do sistema eleitoral antes
      do início da votação, garantindo a lisura do pleito através de duas etapas críticas:

      1. Executa um comando `TRUNCATE` na tabela de votos para eliminar permanentemente
      qualquer registro residual e redefinir os contadores de chaves primárias.

      2. Executa um comando `UPDATE` na tabela de eleitores, resetando o campo
      `status_votacao` para 0 (Não Votou), deixando todos aptos para o pleito.

      Após consolidar as alterações com o `commit`, a função realiza uma consulta relacional
      (`LEFT JOIN` agrupado) para gerar e exibir uma tabela centralizada via Rich, provando
      visualmente ao mesário e aos fiscais que todos os candidatos cadastrados iniciam a
      sessão com exatamente zero votos computados.

      Args:
            None.

      Returns:
            None: A função modifica dados estruturais no banco e exibe o relatório de zeramento
            diretamente no console, aguardando uma interação de teclado para encerrar.
      """
      limpar_tela()

      conexao = cb.conexao_banco()
      cursor = conexao.cursor()

      limpar_tela()
      console.print(Panel(
            Align.center(
                  "[bold bright_white]Verificando e zerando o sistema antes da votação...[/bold bright_white]\n"
                  "[dim]Todos os votos e status dos eleitores serão reiniciados.[/dim]"
            ),
            title="[bold bright_white]INICIANDO ZERÉSIMA[/bold bright_white]",
            border_style="bold green",
            box=box.DOUBLE,
            padding=(1, 4)
      ))
      time.sleep(2)
      limpar_tela()

      truncar_votos = "TRUNCATE votos;"
      cursor.execute(truncar_votos)
      conexao.commit()

      console.print(Panel(
            Align.center(
                  "[bold green]✓[/bold green]  Tabela de votos limpa com sucesso.\n"
                  "[dim]Todos os registros de votos foram eliminados.[/dim]"
            ),
            title="[bold bright_white]VOTOS ZERADOS[/bold bright_white]",
            border_style="bold green",
            box=box.DOUBLE,
            padding=(1, 4)
      ))
      time.sleep(2)
      limpar_tela()

      resetar_status_eleitores = "UPDATE eleitores SET status_votacao = 0;"
      cursor.execute(resetar_status_eleitores)
      conexao.commit()

      console.print(Panel(
            Align.center(
                  "[bold green]✓[/bold green]  Status de votação dos eleitores redefinido.\n"
                  "[dim]Todos os eleitores estão aptos para votar.[/dim]"
            ),
            title="[bold bright_white]ELEITORES RESETADOS[/bold bright_white]",
            border_style="bold green",
            box=box.DOUBLE,
            padding=(1, 4)
      ))
      time.sleep(2)
      limpar_tela()

      console.print(Panel(
            Align.center("[bold green]Zerésima finalizada com sucesso![/bold green]"),
            title="[bold bright_white]ZERÉSIMA CONCLUÍDA[/bold bright_white]",
            border_style="bold green",
            box=box.DOUBLE,
            padding=(1, 4)
      ))
      input("\nPressione Enter para ver o relatório de votos...")
      limpar_tela()

      buscar_candidatos = "SELECT candidatos.nome, candidatos.sigla_partido, COUNT(votos.id) AS total_votos FROM candidatos LEFT JOIN votos ON candidatos.id = votos.id_candidato GROUP BY candidatos.id ORDER BY candidatos.nome;"
      cursor.execute(buscar_candidatos)
      candidatos = cursor.fetchall()

      tabela = Table(
            title="Candidatos — Votos Zerados",
            box=box.DOUBLE,
            border_style="bold sandy_brown",
            title_style="bold bright_white",
            header_style="bold sandy_brown",
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
