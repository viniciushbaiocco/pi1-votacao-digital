"""Função de zerezima para zerar todos os votos registados na tabela de votos.
Também atualiza o status de votação dos eleitores para 'False'(não votou). 
    
    Args: none

    Return: none

    Exibe a lista de candidatos com o total de votos, comprovando a finalização
da zerézima.
"""
from database import conexao_banco as cb


def zerezima():

    print("\nIniciando zerézima...")
    conexao = cb.conexao_banco()
    cursor = conexao.cursor()

    # zerar votos da tabela candidatos
    comando1 = ("DELETE FROM votos;")
    cursor.execute(comando1)
    conexao.commit()
    print("\nEliminando todos os votos registrados na tabela 'Votos'...")

    # atualizar votos eleitores para "false"
    comando2 = ("UPDATE eleitores SET status_votacao = 0;")
    cursor.execute(comando2)
    conexao.commit()
    print("\nAtualizando status de votação de eleitores para 'Não'...")

    print("\nZerézima finalizada!")

    # exibir lista de eleitores
    comando3 = ("SELECT candidatos.nome, candidatos.sigla_partido, COUNT(votos.id) AS total_votos FROM candidatos LEFT JOIN votos ON candidatos.id = votos.id_candidato GROUP BY candidatos.id;")
    cursor.execute(comando3)
    lista_candidatos_zerado = cursor.fetchall()

    print("\n" + "="*10 + "LISTAGEM DE CANDIDATOS E VOTOS" + "="*10)
    print("="*50)
    print(f"{'CANDIDATO':<20} | {'PARTIDO':<10} | {'VOTOS':<5}")
    print("-" * 50)

    for nome, partido, votos in lista_candidatos_zerado:
        print(f"{nome:<20} | {partido:<10} | {votos:<5}")

    print("="*50)

    cursor.close()
    conexao.close()
