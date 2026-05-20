"""
Estatística de Comparecimento

Exibindo:
  - Quantidade total de eleitores que votaram
  - Percentual desse número que realmente votou

"""

from database.conexao_banco import conexao_banco


def exibir_estatistica_comparecimento() -> None:
    """
    Consulta o banco de dados e exibe no terminal a estatística.

    Args:
        None
    Returns:
        None
    """

    conexao = conexao_banco()
    if not conexao:
        print("  [ERRO] Falha na conexão com o banco de dados.")
        return

    cursor = conexao.cursor(dictionary=True)

    # Total de eleitores cadastrados
    cursor.execute("SELECT COUNT(*) AS total FROM eleitores")
    total_eleitores = cursor.fetchone()["total"]

    if total_eleitores == 0:
        print("\n  [AVISO] Nenhum eleitor cadastrado no sistema.")
        cursor.close()
        conexao.close()
        return

    # Total de eleitores que votaram (status_votacao = TRUE)
    cursor.execute(
        "SELECT COUNT(*) AS votaram FROM eleitores WHERE status_votacao = TRUE"
    )
    total_votaram = cursor.fetchone()["votaram"]

    cursor.close()
    conexao.close()

    # Cálculo do percentual de comparecimento
    nao_votaram = total_eleitores - total_votaram
    percentual = (total_votaram / total_eleitores) * 100
    percentual_ausencia = (nao_votaram / total_eleitores) * 100

    # Exibição dos resultados
    print("\n" + "=" * 55)
    print("\tESTATÍSTICA DE COMPARECIMENTO")
    print("=" * 55)
    print(f"  Total de eleitores aptos    : {total_eleitores}")
    print(f"  Eleitores que votaram       : {total_votaram}")
    print(f"  Eleitores ausentes          : {nao_votaram}")
    print("-" * 55)
    print(f"  Percentual de comparecimento: {percentual:.2f}%")
    print(f"  Percentual de abstenção     : {percentual_ausencia:.2f}%")
    print("=" * 55)