from posfixa import OPERADORES
from Automato import get_base
from Automato import Automato

def unicao(automado_a, automado_b):
    automato = Automato()

    automato.add_estado()
    automato.set_inicial(0)
    automato.set_final_automato(1)
    
    numero_estados = 1
    
    for estado in automado_a.estados:
        novas_opcoes = automado_a.get_estado_offset(estado, numero_estados) 
        novo_estado = automato.add_estado(numero=estado+numero_estados, opcoes=novas_opcoes)
        #se o estado é inicial, liga o novo estado inicial a ele e modifica ele para um estado não inicial
        if novas_opcoes["inicial"]:
            automato.add_transicao(automato.estado_inicial, "&", novo_estado)
            automato.set_inicial(novo_estado, inicial=False)

    numero_estados = len(automato)

    for estado in automado_b.estados:
        novas_opcoes = automado_b.get_estado_offset(estado, numero_estados) 
        novo_estado = automato.add_estado(numero=estado+numero_estados, opcoes=novas_opcoes)
        #se o estado é inicial, liga o novo estado inicial a ele e modifica ele para um estado não inicial
        if novas_opcoes["inicial"]:
            automato.add_transicao(automato.estado_inicial, "&", novo_estado)
            automato.set_inicial(novo_estado, inicial=False)
    
    #aponta estados finais para o novo estado final, 
    estado_final = automato.add_estado()

    for estado in automato.estados_finais:
        automato.add_transicao(estado, "&", estado_final)
    
    automato.set_final(estado_final)



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
            if len(pilha) > 0:
                if simbolo == "*":
                    """
                    Operador unario
                    """
                    automato_top = pilha.pop()
                    pilha.append(fecho_kleene(automato_top))
                else:
                    """
                    Operador binario
                    """
                    automato_top_b = pilha.pop()
                    if len(pilha) > 0:
                        automato_top_a = pilha.pop()
                        if simbolo == "+":
                            pilha.append(unicao(automato_top_a, automato_top_b))
                        elif simbolo == ".":
                            pilha.append(concatenacao(automato_top_a, automato_top_b))
                    else:
                        print("pilha vazia na eminencia de uma operação binaria")

            else:
                print("pilha vazia na eminencia de uma operação")
    afd = pilha.pop()
    if len(pilha) <= 0:
        return afd
    else:
        return False

if __name__ == "__main__":
    ken_thompson("asd+.*")