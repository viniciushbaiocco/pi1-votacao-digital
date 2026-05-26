from rich.console import Console
from Visual.visual import limpar_tela
from time import sleep

console = Console(highlight=False)

def validar_titulo(titulo):
    """
    Valida matematicamente um Título de Eleitor verificando seus dois dígitos verificadores e
    verificando o código de UF.
    Args:
        titulo (str): O Título de Eleitor a ser validado, com ou sem espaços.
    Returns:
        bool: True se o Título de Eleitor for válido, False caso contrário.
    """
    # Limpando
    titulo_limpo = titulo.replace(".", "").replace("-", "").replace(" ", "")

    # Letras
    if not titulo_limpo.isdigit():
        console.print("\nTítulo de eleitor inválido! O Título deve conter apenas números.", style="bold red")
        sleep(1.5)
        limpar_tela()
        return False

    digitos = [int(d) for d in titulo_limpo]

    # Tamanho
    if len(digitos) != 12:
        console.print("\nTítulo de eleitor inválido! O Título de eleitor deve conter 12 dígitos.", style="bold red")
        sleep(1.5)
        limpar_tela()
        return False

    # Código de UF
    dicionario_UF = {
        "01": "SP", "02": "MG", "03": "RJ", "04": "RS", "05": "BA",
        "06": "PR", "07": "CE", "08": "PE", "09": "SC", "10": "GO",
        "11": "MA", "12": "PB", "13": "PA", "14": "ES", "15": "PI",
        "16": "RN", "17": "AL", "18": "MT", "19": "MS", "20": "DF",
        "21": "SE", "22": "AM", "23": "RO", "24": "AC", "25": "AP",
        "26": "RR", "27": "TO", "28": "ZZ"
    }

    str_uf = titulo_limpo[8:10]
    uf_d1 = digitos[8]
    uf_d2 = digitos[9]
    codigo_uf = uf_d1 * 10 + uf_d2

    if str_uf not in dicionario_UF:
        console.print("\nTítulo de eleitor inválido!", style="bold red")
        sleep(1.5)
        limpar_tela()
        return False

    # 1 dígito verificador
    pesos_1_DV = [2, 3, 4, 5, 6, 7, 8, 9]
    soma_1_DV  = 0
    for i in range(8):
        soma_1_DV = soma_1_DV + (digitos[i] * pesos_1_DV[i])
    resto_1_DV = soma_1_DV % 11

    if resto_1_DV == 10:
        digito_1_DV = 0
    elif resto_1_DV == 0 and (codigo_uf == 1 or codigo_uf == 2):
        digito_1_DV = 1
    else:
        digito_1_DV = resto_1_DV

    # 2 dígito verificador
    base_2_DV  = [uf_d1, uf_d2, digito_1_DV]
    pesos_2_DV = [7, 8, 9]
    soma_2_DV  = 0
    for i in range(3):
        soma_2_DV = soma_2_DV + (base_2_DV[i] * pesos_2_DV[i])
    resto_2_DV = soma_2_DV % 11

    if resto_2_DV == 10:
        digito_2_DV = 0
    elif resto_2_DV == 0 and (codigo_uf == 1 or codigo_uf == 2):
        digito_2_DV = 1
    else:
        digito_2_DV = resto_2_DV

    # Comparando
    if digitos[10] != digito_1_DV or digitos[11] != digito_2_DV:
        console.print("\nTítulo de eleitor inválido!", style="bold red")
        sleep(1.5)
        limpar_tela()
        return False

    return True
