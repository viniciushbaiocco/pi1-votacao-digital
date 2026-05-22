from database import conexao_banco
from rich.console import Console
from Visual.visual import limpar_tela
from time import sleep

console = Console(highlight=False)

def verificar_candidato(partido, sigla_partido, numero_votacao):

    """
    Verifica a validade de um candidato antes de seu cadastro no banco de dados.
    
    Esta função realiza duas verificações principais:
    
    1. Garante que não haja mais de um candidato associado ao mesmo partido.
    2. Garante que o número de votação proposto ainda não esteja em uso.
    
    Args:
        partido (str): O nome do partido do candidato a ser verificado.
        sigla_partido (str): A sigla do partido do candidato a ser verificado.
        numero_votacao (int): O número de votação do candidato a ser verificado.
        
    Returns:
        bool: True se o candidato for válido para cadastro (partido e número de votação únicos), False caso contrário.
    """

    conexao = conexao_banco.conexao_banco()
    cursor = conexao.cursor()

    query_partido = "SELECT COUNT(*) FROM candidatos WHERE partido = %s"

    cursor.execute(query_partido, (partido,))
    resultado_partido = cursor.fetchone()

    if resultado_partido == (1,):
        limpar_tela()
        console.print("Apenas um candidato por partido é permitido", style="bold yellow")
        sleep(1.5)
        return False

    query_sigla_partido = "SELECT COUNT(*) FROM candidatos WHERE sigla_partido = %s"

    cursor.execute(query_sigla_partido, (sigla_partido,))
    resultado_sigla_partido = cursor.fetchone()

    if resultado_sigla_partido == (1,):
        limpar_tela()
        console.print("Apenas um candidato por partido é permitido", style="bold yellow")
        sleep(1.5)
        return False

    query_numero_votacao = "SELECT COUNT(*) FROM candidatos WHERE numero_votacao = %s"

    cursor.execute(query_numero_votacao, (numero_votacao,))
    resultado_votacao = cursor.fetchone()

    if resultado_votacao == (1,):
        limpar_tela()
        console.print("Número de Votação já cadastrado", style="bold yellow")
        sleep(1.5)
        return False

    cursor.close()
    conexao.close()

    return True
