import os
from datetime import datetime
from colorama import Fore, Style
import os

def ocorrencia_voto_duplo():
    try:
        with open("Voto_Duplo.txt", "a", encoding="utf-8") as arq:
            agora = datetime.now()
            sem_milisegundos = agora.replace(microsecond=0)
            arq.write(Fore.RED + Style.BRIGHT + f"\n[{sem_milisegundos}] ALERTA: Tentativa de Voto Duplo")
    except FileNotFoundError:
        with open("Voto_duplo.txt", "a", encoding="utf-8") as arq:
            arq.write(Fore.RED + Style.BRIGHT + f"\n[{sem_milisegundos}] ALERTA: Tentativa de Voto Duplo")

def imprimir_voto_duplo():
    try:
        with open("Voto_Duplo.txt", "r", encoding="utf-8") as arq:
            conteudo = arq.read()
            print(conteudo)
    except FileNotFoundError:
        print(Fore.YELLOW + Style.BRIGHT +"\nNenhum Log de Voto Duplo Registrado")
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"\nErro ao ler o log de Voto Duplo {e}")

def excluir_arquivo_voto_duplo():
    arquivo = "Voto_Duplo.txt"
    os.remove(arquivo)
