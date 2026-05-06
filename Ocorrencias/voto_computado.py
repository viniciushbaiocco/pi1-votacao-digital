import os
from datetime import datetime
from colorama import Fore, Style
from Verificadores import confirmacao

def voto_computado():
    try:
        with open("Voto_Computado.txt", "a", encoding="utf-8") as arq:
            agora = datetime.now()
            sem_milisegundos = agora.replace(microsecond=0)
            arq.write(Fore.GREEN + Style.BRIGHT + f"\n[{sem_milisegundos}] Voto Computado!")
    except FileNotFoundError:
        with open("Voto_Computado.txt", "a", encoding="utf-8") as arq:
            arq.write(Fore.GREEN + Style.BRIGHT + f"\n[{sem_milisegundos}] Voto Computado!")

def imprimir_voto_computado():
    try:
        with open("Voto_Computado.txt", "r", encoding="utf-8") as arq:
            conteudo = arq.read()
            print(conteudo)
            confirmacao.confirmacao()
    except FileNotFoundError:
        print(Fore.YELLOW + Style.BRIGHT +"\nNenhum Log de Voto Registrado")
        confirmacao.confirmacao()
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"\nErro ao ler o log de Voto {e}")
        confirmacao.confirmacao()

def excluir_arquivo_voto_computado():
    arquivo = "Voto_Computado.txt"
    os.remove(arquivo)