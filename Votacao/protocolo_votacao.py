import random

def gerar_protocolo_votacao(numero_candidato):
    """
    Gera um identificador alfanumérico único para auditoria do voto computado.

    Esta função cria uma assinatura de rastreabilidade (hash de protocolo) para o
    voto através da amalgamação de sementes aleatórias e dados temporais/políticos.
    A estrutura final da string gerada segue o padrão de máscara:
    `V[Letras][Ano][Número_Candidato][Dígitos_Aleatórios]`

    Args:
        numero_candidato (int ou str): O número de votação do candidato (ou '00' para nulo)
        escolhido pelo eleitor, incorporado no corpo do protocolo.

    Returns:
        str: Uma string exclusiva contendo o protocolo de votação formatado para
        registro e conferência de integridade.
    """
    prefixo = "V"
    ano = 26

    # Gera duas letras maiúsculas aleatórias
    letras_aleatorias = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))

    # Gera 5 dígitos aleatórios
    numeros_aleatorios = random.randint(10000, 99999)

    protocolo_votacao = prefixo + letras_aleatorias + str(ano) + str(numero_candidato) + str(numeros_aleatorios)

    return protocolo_votacao
