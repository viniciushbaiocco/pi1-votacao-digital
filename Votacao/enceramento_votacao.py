from Verificadores import verificacao_chave_acesso_banco
from Validadores import validacao_chave_acesso, confirmacao
from database import conexao_banco
from Votacao import autenticacao_mesario
from criptografia import criptografia as cripto
from Ocorrencias import encerramento_urna, geral
from colorama import Fore, Style


def encerrar_sistema_votacao():
    """
    Realiza o encerramento oficial do sistema de votação.

    Args:
        Nenhum.

    Returns:
        bool: True se o encerramento for realizado com sucesso, False caso contrário.
    """
    if autenticacao_mesario.autenticar_mesario() == False:
        return False

    conexao = conexao_banco.conexao_banco() #mudei o import pq o nome tava diferente

    try:
        cursor = conexao.cursor()

        resposta = input(Fore.WHITE + Style.BRIGHT + "\nDeseja realmente encerrar a votação? (Sim/Não): ")
        resposta_sem_espaco = resposta.replace(" ", "")

        if resposta_sem_espaco.lower() != "sim":
            print(Fore.YELLOW + Style.BRIGHT + "\nEncerramento cancelado.") #mudei a msg aqui
            confirmacao.confirmacao()
            return False

        confirmacao_chave = input(Fore.WHITE + Style.BRIGHT + "\nConfirme sua chave de acesso pessoal: ")

        if validacao_chave_acesso.validar_chave_acesso(confirmacao_chave) == False:
            print(Fore.YELLOW + Style.BRIGHT + "\nEncerramento cancelado.")
            confirmacao.confirmacao()
            return False

        confirmacao_chave_criptografada = cripto.criptografar_chave_acesso(confirmacao_chave)

        if verificacao_chave_acesso_banco.verificar_chave_acesso_banco(confirmacao_chave_criptografada) == (0,):
            print(Fore.YELLOW + Style.BRIGHT + "\nChave de acesso não confere. Encerramento cancelado.")
            confirmacao.confirmacao()
            return False

        print(Fore.GREEN + Style.BRIGHT + "\nSistema de votação encerrado.")

        encerramento_urna.ocorrencia_encerramento_urna()
        geral.ocorrencia_encerramento_urna()
        confirmacao.confirmacao()

        return True

    except:
        print(Fore.RED+ Style.BRIGHT + "\nErro ao registrar encerramento.")
        if conexao:
            conexao.rollback()
        return False

    finally:
        if conexao:
            cursor.close()
            conexao.close()
