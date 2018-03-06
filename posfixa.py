
def infixa_posfixa(entrada):
    posfixa = ""
    operadores = {"+", ".", "*", "(", ")"}
    precedencia = {"+":0, ".":1, "*":2}
    pilha = list()
    entrada_1 = None
    entrada_2 = None

    while len(entrada) > 0:


        entrada_1 = entrada_2
        entrada_2 = None

        atual = entrada[0]
        entrada = entrada[1:]

        #ignora espaços
        if atual == " ":
            continue

        if atual in operadores:
            entrada_2 = "operador"

            if atual == "(":

                pilha.append(atual)

            elif atual == ")":

                if len(pilha) > 0:
                    while pilha[0] != "(":
                        posfixa += pilha.pop()
                    if pilha[0] == "(":
                        pilha.pop()
                    else:
                        print("erro, parenteses")
            else:
                if len(pilha) > 0:
                    while precedencia[atual] <= precedencia[pilha[0]]:
                        posfixa += pilha.pop()
                pilha.append(atual)
        else:
            posfixa += atual
            entrada_2 = "operando"

            if entrada_1 == entrada_2 and entrada_1 == "operando":
                # concatenação implicita
                if len(pilha) > 0:
                    while precedencia["."] <= precedencia[pilha[0]]:
                        posfixa += pilha.pop()
                pilha.append(".")
        print(pilha)
        print(posfixa)

    while len(pilha) > 0:
        posfixa += pilha.pop()

    print(pilha)
    print(posfixa)



infixa_posfixa("(a + b) * c")