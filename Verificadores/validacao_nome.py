def validar_nome():

    nome_validado = False
    while not nome_validado:

        nome = str(input("Digite nome: "))
        nome_ajustado = nome.split()

        if len(nome_ajustado) < 2:
            nome_validado = False
            print("Nome inválido! Necessário nome completo (nome e sobrenome).")
        else:

            if len(nome_ajustado[0]) < 2:
                nome_validado = False
                print(
                    "Nome inválido! Primeiro nome precisa ter mínimo de 3 letras.")
            else:
                if len(nome_ajustado[1]) < 1:
                    nome_validado = False
                    print(
                        "Sobrenome inválido! Sobrenome precisa ter mínimo de 2 letras.")
                else:
                    nome_validado = True

    return nome_validado


if __name__ == "__main__":
    nome_check = validar_nome()
    print(nome_check)