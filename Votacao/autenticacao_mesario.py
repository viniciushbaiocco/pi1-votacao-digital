from colorama import Fore, Style, init
from Validadores import validacao_titulo as val_tit
from Validadores import validacao_cpf_votacao as val_cpf_vot
from Validadores import validacao_chave_acesso as val_chave
from Verificadores import verificacao_mesario_banco as ver_mes
from Ocorrencias import acesso_negado
from criptografia import criptografia as crip

init(autoreset=True)

def autenticar_mesario():
    """
    Solicita e valida os dados do mesário para abertura da votação:
    título de eleitor, 4 primeiros dígitos do CPF e chave de acesso.

    Args:
        None

    Returns:
        bool: True se o mesário for validado com sucesso, False caso contrário.
    """
    print(Fore.CYAN + Style.BRIGHT + '\n--- Identificação do Mesário ---')

    # recolher e validar título de eleitor
    titulo = input(Fore.WHITE + Style.BRIGHT + '\nDigite seu Título de Eleitor: ')
    while val_tit.validar_titulo(titulo) == False:
        titulo = input(Fore.WHITE + Style.BRIGHT + '\nDigite seu Título de Eleitor novamente: ')

    # recolher e validar os 4 primeiros dígitos do CPF
    cpf_4 = input(Fore.WHITE + Style.BRIGHT + '\nDigite os 4 primeiros dígitos do seu CPF: ')
    while val_cpf_vot.validar_cpf_voto(cpf_4) == False:
        cpf_4 = input(Fore.WHITE + Style.BRIGHT + '\nDigite os 4 primeiros dígitos do seu CPF novamente: ')

    # recolher e validar chave de acesso
    chave_acesso = input(Fore.WHITE + Style.BRIGHT + '\nDigite sua Chave de Acesso: ').upper()
    while val_chave.validar_chave_acesso(chave_acesso) == False:
        chave_acesso = input(Fore.WHITE + Style.BRIGHT + '\nDigite sua Chave de Acesso novamente: ').upper()

    # criptografar e verificar no banco de dados
    cpf_4_criptografado = crip.criptografar_cpf(cpf_4)
    chave_acesso_criptografada = crip.criptografar_chave_acesso(chave_acesso)

    resultado = ver_mes.verificar_mesario(titulo, cpf_4_criptografado, chave_acesso_criptografada)

    if resultado == (1,):
        print(Fore.GREEN + Style.BRIGHT + '\nMesário validado com sucesso! Sistema de votação aberto.')
        return True
    else:
        print(Fore.RED + Style.BRIGHT + '\nDados inválidos. Acesso negado.')
        acesso_negado.ocorrencia_acesso_negado()
        return False
