from posfixa import OPERADORES
from Automato import get_base
from Automato import Automato

def une_alfabetos(a, b):
    novo_alfabeto = list()
    for i in a:
        novo_alfabeto.append(i)
    for i in b:
        novo_alfabeto.append(i)
    
    return novo_alfabeto

def uniao(automato_a, automato_b):
    automato = Automato()
    estado_inicial = automato.add_estado()
    automato.set_inicial(estado_inicial)
    
    #une os alfabetos
    automato.set_alfabeto(une_alfabetos(automato_a.alfabeto, automato_b.alfabeto))

    numero_estados = 1
    
    for estado in list(automato_a.estados):
        novas_opcoes = automato_a.get_estado_offset(estado, numero_estados)
        inicial = novas_opcoes["inicial"]
        novas_opcoes["inicial"] = False
        novo_estado = automato.add_estado(numero=estado+numero_estados, opcoes=novas_opcoes)
        #se o estado é inicial, liga o novo estado inicial a ele e modifica ele para um estado não inicial
        if inicial:
            print("aqui não")
            automato.add_transicao(automato.estado_inicial, "&", novo_estado)

    numero_estados = len(automato)

    for estado in list(automato_b.estados):
        novas_opcoes = automato_b.get_estado_offset(estado, numero_estados) 
        inicial = novas_opcoes["inicial"]
        novas_opcoes["inicial"] = False
        novo_estado = automato.add_estado(numero=estado+numero_estados, opcoes=novas_opcoes)
        #se o estado é inicial, liga o novo estado inicial a ele e modifica ele para um estado não inicial
        if inicial:
            automato.add_transicao(automato.estado_inicial, "&", novo_estado)
            print("aqui sim")
    
    #aponta estados finais para o novo estado final, 
    estado_final = automato.add_estado()

    for estado in automato.estados_finais:
        automato.add_transicao(estado, "&", estado_final)
        automato.set_final(estado, final=False)
    
    automato.set_final_automato(estado_final)

    return automato


def concatenacao(automato_a, automato_b):
    #une os alfabetos
    automato_a.set_alfabeto(une_alfabetos(automato_a.alfabeto, automato_b.alfabeto))
    estado_inicial = automato_a.estado_inicial
    offset_estados = len(automato_a)

    for estado in list(automato_b.estados):
        novas_opcoes = automato_b.get_estado_offset(estado, offset_estados)
        novo_estado = automato_a.add_estado(estado + offset_estados, opcoes=novas_opcoes)

        if novas_opcoes["inicial"]:
            automato_a.add_transicao(automato_a.estado_final, "&", novo_estado)
            automato_a.set_inicial(novo_estado, inicial=False)
        
        if novas_opcoes["final"]:
            automato_a.set_final(automato_a.estado_final, final=False)
            automato_a.set_final_automato(novo_estado)
    automato_a.set_inicial(estado_inicial)
    return automato_a

def fecho_kleene(automato):

    novo_automato = Automato()
    novo_automato.add_estado()
    novo_automato.set_inicial(0)
    
    offset_estados = 1
    final_velho = None
    inicial_velho = None

    for estado in list(automato.estados):
        novas_opcoes = automato.get_estado_offset(estado, offset_estados)
        novo_estado = novo_automato.add_estado(offset_estados + estado, opcoes=novas_opcoes)

        if novas_opcoes["inicial"]:
            inicial_velho = novo_estado
            novo_automato.set_inicial(novo_estado, inicial=False)
        
        if novas_opcoes["final"]:
            final_velho = novo_estado
            novo_automato.set_final(novo_estado, final=False)
    
    novo_automato.add_transicao(novo_automato.estado_inicial, "&", inicial_velho)

    novo_automato.add_transicao(final_velho, "&", inicial_velho)

    novo_automato.add_transicao(final_velho, "&", inicial_velho)

    final_novo = novo_automato.add_estado()
    novo_automato.set_final_automato(final_novo)

    novo_automato.add_transicao(final_velho, "&", final_novo)

    novo_automato.add_transicao(novo_automato.estado_inicial, "&", final_novo)
    
    return novo_automato


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
                    #Operador unario, Fecho de Kleene
                    automato_top = pilha.pop()
                    pilha.append(fecho_kleene(automato_top))
                else:
                    #Operador binario
                    automato_top_b = pilha.pop()
                    print("bbb:", automato_top_b.alfabeto)
                    print(automato_top_b)
                    if len(pilha) > 0:
                        automato_top_a = pilha.pop()
                        print("aaa:", automato_top_a.alfabeto)
                        print(automato_top_a)
                        if simbolo == "+":
                            pilha.append(uniao(automato_top_a, automato_top_b))
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
    from posfixa import infixa_posfixa
    posfixa = infixa_posfixa("ab*")
    print("posfixa: ",posfixa)
    afd = ken_thompson(posfixa)
    print(afd)