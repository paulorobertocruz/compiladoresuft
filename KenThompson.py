from .posfixa import OPERADORES
from .Automato import get_base

def unicao(automado_a, automado_b):
    pass

def concatenacao(automato_a, automato_b):
    pass

def fecho_kleene(automado):
    pass

def ken_thompson(expressao_posfixa):
    pilha = []
    while len(expressao_posfixa) > 0:
        simbolo = expressao_posfixa[0]
        expressao_posfixa = expressao_posfixa[1:]

        if simbolo not in OPERADORES:
            pilha.append(get_base(simbolo))
        else:
            pass