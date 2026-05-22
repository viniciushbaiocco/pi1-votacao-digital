from database import conexao_banco as cb
from Visual.visual import limpar_tela, carregar_pontos_loop
from rich.console import Console
from rich.table import Table
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

      carregar_pontos_loop(3, "Iniciando Zerésima")

      truncar_votos = "TRUNCATE votos;"
      cursor.execute(truncar_votos)
      conexao.commit()
      carregar_pontos_loop(2, "\nEliminando todos os votos registrados na tabela 'Votos'")

      resetar_status_eleitores = "UPDATE eleitores SET status_votacao = 0;"
      cursor.execute(resetar_status_eleitores)
      conexao.commit()
      carregar_pontos_loop(2, "\nAtualizando status de votação de eleitores para 'Não'")

      console.print("\n[bold green]\nZerésima finalizada![/bold green]\n")

      buscar_candidatos = "SELECT candidatos.nome, candidatos.sigla_partido, COUNT(votos.id) AS total_votos FROM candidatos LEFT JOIN votos ON candidatos.id = votos.id_candidato GROUP BY candidatos.id;"
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
