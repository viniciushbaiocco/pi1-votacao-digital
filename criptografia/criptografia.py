ALFABETO = "ZABCDEFGHIJKLMNOPQRSTUVWXY0123456789" #Alfabeto com Z=0 e A=1
MODULO = 36

MATRIZ_CHAVE = [
    [5, 8],
    [17, 3]
]
'''
Matriz-chave 2x2 = [5 8; 17 3]; de acordo com requisito
det = 23; é invertível
'''



# ------------------------------------------------------------
# Funções matemáticas
# ------------------------------------------------------------



def mdc(a: int, b: int):
    while b:
        a, b = b, a % b
    return a

''' 
Calcula o MDC dde a e b

Args:
    a (int): Primeiro numero
    b (int): segundo numero

Returns:
    int: o MDC em a
''' 

def inverso_modular(a: int, m: int):
    if mdc(a, m) != 1:
        raise ValueError(
            f"Inverso modular de {a} em mod {m} não existe. "
            f"mdc({a}, {m}) = {mdc(a, m)} ≠ 1."
        )

    # Algoritmo estendido de Euclides
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

"""
Calcula o inverso modular de 'a' no módulo 'm' com 
Euclides ou famoso pmodulo do SciLab

Args:
    a (int): Valor do inverso modular que é calculado.
    m (int): O módulo.

Returns:
        int: O inverso modular de a em mod m.

Raises:
    ValueError: Se o inverso modular não existir (mdc(a, m) != 1).
"""

def inversa_matriz_2x2(matriz: list, mod: int):
    a, b = matriz[0][0], matriz[0][1]
    c, d = matriz[1][0], matriz[1][1]

    det = (a * d - b * c) % mod
    inv_det = inverso_modular(det, mod)

    inversa = [
        [(inv_det * d) % mod,  (inv_det * (-b)) % mod],
        [(inv_det * (-c)) % mod, (inv_det * a) % mod]
    ]
    return inversa

def multiplicar_matriz_vetor(matriz: list, vetor: list, mod: int):
    resultado = [
        (matriz[0][0] * vetor[0] + matriz[0][1] * vetor[1]) % mod,
        (matriz[1][0] * vetor[0] + matriz[1][1] * vetor[1]) % mod
    ]
    return resultado

"""
Multiplica uma matriz 2x2 por um vetor 2x1.

Args:
    matriz (list): Matriz 2x2. (lista de listas)
    vetor (list): Vetor com 2 inteiros. (v0, v1)
    mod (int): Valor do alfabeto. (no nosso caso, 36)

Returns:
    list: Vetor resultante com 2 inteiros resultado da multiplicação modular.
    """



# ------------------------------------------------------------
#Funções de conversão de texto
# ------------------------------------------------------------



def texto_para_numeros(texto: str):
    resultado = []
    for char in texto.upper():
        if char not in ALFABETO:
            raise ValueError(
                f"Caractere '{char}' não pertence ao alfabeto da Cifra de Hill. "
                f"Use apenas letras (A-Z) e dígitos (0-9)."
            )
        resultado.append(ALFABETO.index(char))
    return resultado

"""
Converte uma string de caracteres em uma lista de números inteiros.
 
Cada caractere é mapeado para seu índice no ALFABETO (list): (Z=0, A=1, [...] 0=26, [...], 9=35).
 
Args:
    texto (str): String contendo apenas caracteres presentes no ALFABETO.
 
   Returns:
    list: Lista de inteiros representando os índices dos caracteres.
 
Raises:
    ValueError: Se digitar texto que não  está no ALFABETO.
"""

 

def numeros_para_texto(numeros: list):
    return "".join(ALFABETO[n % MODULO] for n in numeros)

"""
Convertede volta uma lista de numeros inteiros para uma string de caracteres.

Args:
    numeros (list): Lista de inteiros, cada um no intervalo [0, MODULO-1].

Returns:
    str: String resultante com os caracteres correspondentes aos índices.
"""

 
def duplicar_ultimo(texto: str):
    if len(texto) % 2 != 0:
        return texto + texto[-1]
    return texto

"""
Duplica o último caractere do texto se tiver len() ímpar para não quebrar a metemática

Args:
    texto (str): Texto de entrada que pode ter comprimento par ou ímpar.
 
Returns:
    str: Texto com comprimento par, com ultimo caracter duplicado.
"""



# ------------------------------------------------------------
#Funções Criptografia e Descriptografia
# ------------------------------------------------------------



def criptografar(texto: str) -> str:
    texto = texto.upper()
    texto = duplicar_ultimo(texto)
    numeros = texto_para_numeros(texto)
 
    resultado = []
    # Processa em vetores de 2
    for i in range(0, len(numeros), 2):
        vetor = [numeros[i], numeros[i + 1]]
        vetor_cifrado = multiplicar_matriz_vetor(MATRIZ_CHAVE, vetor, MODULO)
        resultado.extend(vetor_cifrado)
 
    return numeros_para_texto(resultado)
 
"""
Criptografa usando Cifra de Hill com MATRIZ_CHAVE 2x2.
 
Etapas:
    1. Converte o texto para maiúsculao e duplica o último caractere se necessário.
    2. Divide em vetores de 2 caracteres.
    3. Converte cada vetor para um vetor numérico.
    4. Multiplica pela MATRIZ_CHAVE com módulo 36.
    5. Converte os números resultantes de volta para caracteres. (fim da cifra)

Args:
    texto (str): Texto que será cifrado.
 
Returns:
    str: Texto cifrado.
 

Raises:
    ValueError: Se digitar texto que não  está no ALFABETO.
"""

def descriptografar(texto_cifrado: str):
    texto_cifrado = texto_cifrado.upper()
    matriz_inversa = inversa_matriz_2x2(MATRIZ_CHAVE, MODULO)
    numeros = texto_para_numeros(texto_cifrado)
 
    resultado = []
    for i in range(0, len(numeros), 2):
        vetor = [numeros[i], numeros[i + 1]]
        vetor_decifrado = multiplicar_matriz_vetor(matriz_inversa, vetor, MODULO)
        resultado.extend(vetor_decifrado)
 
    return numeros_para_texto(resultado)

"""
Descriptografa o texto cifrado.
 
Etapas:
    1. Calcula a matriz inversa da MATRIZ_CHAVE com módulo 36.
    2. Divide o texto cifrado em vetores de 2 caracteres, assim como na cifra.
    3. Converte cada vetor para vetor numérico.
    4. Multiplica pela matriz inversa com módulo 36.
    5. Converte de volta para string.
 
Args:
    texto_cifrado (str): Texto cifrado, gerado criptografia.
 
Returns:
    str: Texto original descriptografado (com final duplicado ou não).
 
Raises:
    ValueError: Se digitar texto que não  está no ALFABETO.
"""



# ------------------------------------------------------------
#Criptografia e Descriptografia | CPF
# ------------------------------------------------------------



def criptografar_cpf(cpf: str):
    cpf_limpo = cpf.replace(".", "").replace("-", "")
    return criptografar(cpf_limpo)

"""
Criptografa o CPF do eleitor.

Remove pontos e traços do CPF formatado antes de cifrar,
garantindo que apenas dígitos (0-9) sejam processados. (feature)

Args:
    cpf (str): CPF do eleitor no formato '12345678901' ou '123.456.789-01'.

Returns:
    str: CPF criptografado.
"""

 
 
def descriptografar_cpf(cpf_cifrado: str):
    return descriptografar(cpf_cifrado)

"""
Descriptografa o CPF.

Args:
    cpf_cifrado (str): CPF criptografado, por criptografar_cpf().

Returns:
    str: CPF original com 11 dígitos sem formatação.
"""

# ------------------------------------------------------------
#Criptografia - Chave de acesso
# ------------------------------------------------------------


 
def criptografar_chave_acesso(chave: str):
    return criptografar(chave)

"""
Criptografa a chave de acesso do eleitor.

Args:
    chave (str): Chave de acesso do eleitor.

Returns:
    str: Chave de acesso criptografada.
"""

 
def descriptografar_chave_acesso(chave_cifrada: str):
    return descriptografar(chave_cifrada)

"""
Descriptografa a chave de acesso do eleitor.

Args:
    chave_cifrada (str): Chave de acesso do eleitor cifrada.

Returns:
    str: Chave de acesso descriptografada.
"""



# ------------------------------------------------------------
#Criptografia - Protocolo
# ------------------------------------------------------------



def criptografar_protocolo(protocolo: str):
    return criptografar(protocolo)
"""
Criptografa o protocolo de votação.

O protocolo segue o padrão: 'V' + 2 letras aleatórias + ano (2 dígitos) + número do candidato (2 dígitos) + 5 dígitos aleatórios.

Args:
    protocolo (str): Protocolo de votação gerado no voto.

Returns:
    str: Protocolo criptografado.
"""
 
def descriptografar_protocolo(protocolo_cifrado: str):
    return descriptografar(protocolo_cifrado)

"""
Descriptografa o protocolo de votação.

Args:
    protocolo_cifrado (str): Protocolo criptografado.

Returns:
    str: Protocolo de votação descriptografado.
"""