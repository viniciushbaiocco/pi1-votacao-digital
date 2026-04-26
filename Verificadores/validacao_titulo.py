def validar_titulo (titulo):

    arrumando = titulo.replace(" ", "")

    #Verificação de tamanho do título
    if  len(arrumando) != 12:
        print("Erro: O Título de eleitor deve conter 12 dígitos.")
        return False
    
     #Verificação se tem letras
    try:
        separado = [int(i) for i in arrumando]
    
    except ValueError:
        print("Erro: O Título deve conter apenas números.")
        return False

    dicionario_UF = {
    "01": "SP","02": "MG","03": "RJ","04": "RS","05": "BA","06": "PR","07": "CE","08": "PE","09": "SC",
    "10": "GO","11": "MA","12": "PB","13": "PA","14": "ES","15": "PI","16": "RN","17": "AL","18": "MT",
    "19": "MS","20": "DF","21": "SE","22": "AM","23": "RO","24": "AC","25": "AP","26": "RR","27": "TO",
    "28": "ZZ"
    }
    str_uf    = arrumando[8:10]
    uf_d1     = separado[8]
    uf_d2   = separado[9]
    codigo_uf = uf_d1 * 10 + uf_d2
 
    if str_uf not in dicionario_UF:
        print(f"Erro: Código de UF inválido")
        return False

    lista_1_DV = [2, 3, 4, 5, 6, 7, 8, 9]
    soma_1_DV  = 0
    for i in range(8):
        soma_1_DV = soma_1_DV + (separado[i] * lista_1_DV[i])
 
    resto_1_DV = soma_1_DV % 11
 
    if resto_1_DV == 10:
        digito_1_DV = 0
    elif resto_1_DV == 0 and (codigo_uf == 1 or codigo_uf == 2):
        digito_1_DV = 1
    else:
        digito_1_DV = resto_1_DV
 
    lista_2_DV = [7, 8, 9]
    soma_2_DV  = 0
    nova_lista  = [uf_d1, uf_d2, digito_1_DV]
 
    for i in range(3):
        soma_2_DV = soma_2_DV + (nova_lista[i] * lista_2_DV[i])
 
    resto_2_DV = soma_2_DV % 11
 
    if resto_2_DV == 10:
        digito_2_DV = 0
    elif resto_2_DV == 0 and (codigo_uf == 1 or codigo_uf == 2):
        digito_2_DV = 1
    else:
        digito_2_DV = resto_2_DV
 
    if separado[10] != digito_1_DV or separado[11] != digito_2_DV:
        print("Erro: Dígitos verificadores errados")
        return False
 
    print(f"Título de eleitor válido!")
    return True