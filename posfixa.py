
def infixa_posfixa(entrada):

    #remove espaços
    entrada = entrada.replace(" ", "")
    print(entrada)
    posfixa = ""
    operadores = {"+", ".", "*", "(", ")"}
    precedencia = {"+":0, ".":1, "*":2, "(":99, ")":99}
    pilha = list()
    entrada_1 = None
    entrada_2 = None

    while len(entrada) > 0:
        entrada_1 = entrada_2
        entrada_2 = None

        atual = entrada[0]
        entrada = entrada[1:]

        if atual in operadores:
            entrada_2 = "operador"

            if atual == "(":
                pilha.append(atual)

            elif atual == ")":
                if len(pilha) > 0:
                    while len(pilha) > 0 and pilha[-1] != "(":
                        posfixa += pilha.pop()
                    if len(pilha) > 0 and pilha[-1] == "(":
                        pilha.pop()
                    else:
                        print("erro, parenteses")
            else:
                while len(pilha) > 0 and precedencia[atual] <= precedencia[pilha[-1]] and pilha[-1] not in {"(", ")"}:
                    posfixa += pilha.pop()
                pilha.append(atual)
        else:
            posfixa += atual
            entrada_2 = "operando"

            if entrada_1 == entrada_2 and entrada_1 == "operando":
                while len(pilha) > 0 and precedencia["."] <= precedencia[pilha[-1]] and pilha[-1] not in {"(", ")"}:
                    posfixa += pilha.pop()
                pilha.append(".")
        print(pilha)
        print(posfixa)

    while len(pilha) > 0:
        posfixa += pilha.pop()

    print(pilha)
    print(posfixa)



infixa_posfixa("(a + b) * c")