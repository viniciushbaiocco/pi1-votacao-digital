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

    try:
        cursor.execute("SELECT COUNT(*) FROM candidatos WHERE partido = %s", (partido,))
        if cursor.fetchone()[0] > 0:
            limpar_tela()
            console.print("Apenas um candidato por partido é permitido", style="bold yellow")
            sleep(1.5)
            return False

        cursor.execute("SELECT COUNT(*) FROM candidatos WHERE sigla_partido = %s", (sigla_partido,))
        if cursor.fetchone()[0] > 0:
            limpar_tela()
            console.print("Apenas um candidato por partido é permitido", style="bold yellow")
            sleep(1.5)
            return False

        cursor.execute("SELECT COUNT(*) FROM candidatos WHERE numero_votacao = %s", (numero_votacao,))
        if cursor.fetchone()[0] > 0:
            limpar_tela()
            console.print("Número de Votação já cadastrado", style="bold yellow")
            sleep(1.5)
            return False

        return True

    finally:
        cursor.close()
        conexao.close()
