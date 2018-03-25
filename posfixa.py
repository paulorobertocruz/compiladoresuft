OPERADOR = 0
OPERANDO = 1
OPERADORES = {"+", ".", "*", "(", ")"}
PRECEDENCIA = {"+":0, ".":1, "*":2, "(":99, ")":99}


class Opera(object):
    """
    Operador ou Operando
    """

    str = None
    tipo = None

    def __init__(self, str, tipo=OPERADOR):
        self.str = str
        self.tipo = tipo

    def __str__(self):
        return "({0} {1})".format(self.str, self.operando_ou_operador())

    def __repr__(self):
        return "({0} {1})".format(self.str, self.operando_ou_operador())

    def operando_ou_operador(self):
        if self.tipo == OPERADOR:
            return "operador"
        else:
            return "operando"

    def igual(self, caractere):
        return self.str == caractere


class Expressao(object):
    lista = []

    def add(self, opera):
        self.lista.append(opera)

    def pop(self):
        if len(self.lista) > 0:
            op = self.lista[0]

        if len(self.lista) > 1:
            self.lista = self.lista[1:]
        else:
            self.lista = []

        return op

    def __len__(self):
        return len(self.lista)

    def __str__(self):
        rr = ""
        for i in self.lista:
            rr += i.str
        return rr


def contra_barra(caractere):
    if caractere in OPERADORES or caractere == "\\":
        return True
    return False


def expressao_lista_opera(expressao):
    expressao = expressao.replace(" ", "")
    operadores = {"+", ".", "*", "(", ")"}
    lista_opera = list()
    express = Expressao()

    while len(expressao) > 0:
        ex_op = None

        expressao_1 = None
        if expressao[0] == "\\":
            if len(expressao) > 1:
                expressao_1 = expressao[1]
            else:
                print("erro, não tem caractere depois da barra")
                return None

            if len(expressao) > 2:
                expressao = expressao[:1] + expressao[2:]
            else:
                expressao = expressao[0]

        if len(expressao) > 1:

            # a.a
            if expressao[0] not in operadores and expressao[1] not in operadores:
                ex_op = Opera(".", tipo=OPERADOR)

            # a.(
            elif expressao[0] not in operadores and expressao[1] == "(":
                ex_op = Opera(".", tipo=OPERADOR)

            # ).a
            elif expressao[0] == ")" and expressao[1] not in operadores:
                ex_op = Opera(".", tipo=OPERADOR)

            # ).(
            elif expressao[0] == ")" and expressao[1] == "(":
                ex_op = Opera(".", tipo=OPERADOR)

            # *.a
            elif expressao[0] == "*" and expressao[1] not in operadores:
               ex_op = Opera(".", tipo=OPERADOR)

            # *.(
            elif expressao[0] == "*" and expressao[1] == "(":
                ex_op = Opera(".", tipo=OPERADOR)


        if expressao[0] in operadores:
            op = Opera(expressao[0], tipo=OPERADOR)
            lista_opera.append(op)
            express.add(op)
            expressao = expressao[1:]

        elif expressao[0] == "\\":
            #pronblema de comparação
            op = Opera( "{0}{1}".format(expressao[0], expressao_1), tipo=OPERANDO)
            lista_opera.append(op)
            express.add(op)
            expressao = expressao[1:]

        else:
            op = Opera(expressao[0], tipo=OPERANDO)
            lista_opera.append(op)
            express.add(op)
            expressao = expressao[1:]

        if ex_op is not None:
            lista_opera.append(ex_op)
            express.add(ex_op)

    return express

def infixa_posfixa(entrada):

    expressao = expressao_lista_opera(entrada)
    print(expressao)
    posfixa = ""

    pilha = list()

    while len(expressao) > 0:

        atual = expressao.pop()

        if atual.tipo == OPERADOR:

            if atual.igual("("):
                pilha.append(atual)
            elif atual.igual(")"):
                if len(pilha) > 0:
                    while len(pilha) > 0 and not pilha[-1].igual("("):
                        posfixa += pilha.pop().str
                    if len(pilha) > 0 and pilha[-1].igual("("):
                        pilha.pop()
                    else:
                        print("erro, parenteses")
            else:
                while len(pilha) > 0 and PRECEDENCIA[atual.str] <= PRECEDENCIA[pilha[-1].str] and pilha[-1].str not in {"(", ")"}:
                    posfixa += pilha.pop().str
                pilha.append(atual)
        else:
            posfixa += atual.str

    while len(pilha) > 0:
        posfixa += pilha.pop().str

    return posfixa


if __name__ == "__main__":
    aaa = "(0+(1(01*(00)*0)*1)*)*"
    print(aaa)
    r = infixa_posfixa(aaa)
    print(r)




































