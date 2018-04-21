
from operator import itemgetter, attrgetter

class SimboloNotExist(Exception):
    pass

class EstadoNotExist(Exception):
    pass

def nome_de_estado_lista(lista):
    nome = ""
    for i in lista:
        nome += "{0}".format(i)
    return nome

def is_novo(dicinario):
    novo = False
    for k in dicinario:
        if "novo" in dicinario[k]:
            if dicinario[k]["novo"] == True:
                novo = True
    
    return novo

class Automato(object):
    alfabeto = None
    estados = None
    estado_inicial = None
    estado_final = None

    fechos = None

    def __init__(self):
        self.alfabeto = list()
        self.estados = dict()
        self.fechos = dict()
    
    def __repr__(self):
        return self.alfabeto.__repr__()

    def __str__(self):
        return_str = ""
        for estado in self.estados:
            if estado < 10:
                return_str += "q0{0}:".format(estado)
            else:
                return_str += "q{0}:".format(estado)

            return_str += "({0}:{1})".format("inicial", self.estados[estado]["inicial"])
            return_str += "({0}:{1})".format("final", self.estados[estado]["final"])

            for ops in self.estados[estado]:
                if ops not in ["final", "inicial"]:
                    return_str += "({0}:{1})".format(ops, self.estados[estado][ops])
            return_str += "\n"

        return return_str
    
    def __len__(self):
        return len(self.estados)

    def set_alfabeto(self, alfa):
        self.alfabeto = alfa

    def add_estado(self, numero = None, opcoes = {}):
    
        if "inicial" not in opcoes:
            opcoes["inicial"] = False

        if "final" not in opcoes:
            opcoes["final"] = False
        
        if numero is not None:
            numero = int(numero)
        else:
            numero = len(self.estados)
        
        self.estados[numero] = dict(opcoes)

        if self.estados[numero]["inicial"]:
            self.set_inicial(numero)
        
        return numero
    
    def get_estado_offset(self, estado, offset):
        novas_opcoes = {}
        for opt in self.estados[estado]:
            if opt not in ["final", "inicial"]:
                novas_opcoes[opt] = list()
                for q in self.estados[estado][opt]:
                    novas_opcoes[opt].append(q + offset)
        
        novas_opcoes["inicial"] = self.estados[estado]["inicial"]
        novas_opcoes["final"] = self.estados[estado]["final"]
        return novas_opcoes

    
    def add_transicao(self, estado_entrada, simbolo, estado_saida):
        if estado_entrada in self.estados and estado_saida in self.estados:
            
            #se não é uma lista instancia uma lista    
            if simbolo not in self.estados[estado_entrada]:
                self.estados[estado_entrada][simbolo] = list()
            
            # se não está nos destinos possiveis adiciona
            if estado_saida not in self.estados[estado_entrada][simbolo]:    
                self.estados[estado_entrada][simbolo].append(estado_saida)
            
            if simbolo not in self.alfabeto:
                self.alfabeto.append(simbolo)
            return True
        else:
            return False
    
    def transicao_afn(self, estado, simbolo):
    
        if estado in self.estados:
            if simbolo in self.estados[estado]:
                return self.estados[estado][simbolo]
            else:
                raise SimboloNotExist
        else:
            raise EstadoNotExist

    def set_inicial(self, estado, inicial = True):
        if estado in self.estados:
            
            if not inicial:
                self.estados[estado]["inicial"] = False
                return True

            if self.estado_inicial is not None: 
                self.estados[self.estado_inicial]["inicial"] = False
            
            self.estado_inicial = estado
            self.estados[estado]["inicial"] = True
            return True
        else:
            return False
    
    def set_final(self, estado, final = True):
        if estado in self.estados:
            if not final:
                self.estados[estado]["final"] = False
                return True
            self.estados[estado]["final"] = True
            return True
        else:
            return False

    def set_final_automato(self, estado):
        if self.set_final(estado):
            self.estado_final = estado
        else:
            return False
    @property
    def estados_finais(self):
        finais = []
        for estado in self.estados:
            if self.estados[estado]["final"]:
                finais.append(estado)
        return finais
    
    def reset_fechos(self):
        self.fechos = {}

    def fecho_e(self, estado):
        
        fecho = list()

        if estado not in self.fechos:
            
            fecho.append(estado)
            
            try:
                transi_e = self.transicao_afn(estado, "&")
            except SimboloNotExist:
                transi_e = []
            
            for t in transi_e:
                t_fechos = self.fecho_e(t)
                for f in t_fechos:
                    if f not in fecho:
                        fecho.append(f)
            
            fecho.sort()
            self.fechos[estado] = fecho

        return self.fechos[estado]
    
    def afd_from_afn(self):
        total_estados = 0
        novo_automato = dict()
        lista_nome_estados = dict()
        lista_estados = list()

        fecho_e_inicial = self.fecho_e(self.estado_inicial)
        lista_estados.append(fecho_e_inicial)
        nome_fecho_e_inicial = nome_de_estado_lista(fecho_e_inicial)
        lista_nome_estados[nome_fecho_e_inicial] = len(lista_estados) - 1
        
        while(len(lista_estados) > 0):
            final = False
            estado_atual = lista_estados.pop(0)

            nome_estado_atual = nome_de_estado_lista(estado_atual)
            lista_nome_estados.pop(nome_estado_atual)

            novo_estado = {}        
            novo_estado["inicial"] = False
            novo_estado["final"] = False

            novo_alfabeto = list()

            for a in self.alfabeto:
                if a == "&":
                    continue
                novo_alfabeto.append(a)

            for e in estado_atual:
                if e in self.estados_finais:
                    novo_estado["final"] = True
                    break
            
            for e in estado_atual:
                if e == self.estado_inicial:
                    novo_estado["inicial"] = True
                    break

            for simbolo in novo_alfabeto:
                conjunto_estados = list()
                for estado in estado_atual:
                    try:
                        transi_e = self.transicao_afn(estado, simbolo)
                    except SimboloNotExist:
                        transi_e = []
                    except EstadoNotExist:
                        transi_e = []
                    for e in transi_e:
                        if e not in conjunto_estados:
                            e_fecho_e = self.fecho_e(e)
                            for ef in e_fecho_e:
                                conjunto_estados.append(ef)
                
                conjunto_estados.sort()
                if conjunto_estados == []:
                    conjunto_estados.append("$")
                
                novo_estado[simbolo] = conjunto_estados
                
                nome_conjunto_estados = nome_de_estado_lista(conjunto_estados)

                if nome_conjunto_estados not in lista_nome_estados and nome_conjunto_estados not in novo_automato:
                    lista_estados.append(conjunto_estados)
                    lista_nome_estados[nome_conjunto_estados] = len(lista_estados) - 1
            
            novo_estado["order"] = total_estados
            
            total_estados += 1
            
            if nome_estado_atual not in novo_automato:
                novo_automato[nome_estado_atual] = novo_estado
        
        
        automato_renomeado = {}
        for e in novo_automato:
            estado_renomeado = {}
            nome_estado = novo_automato[e]["order"]
            estado_renomeado["final"] = novo_automato[e]["final"]
            estado_renomeado["inicial"] = novo_automato[e]["inicial"]

            for a in novo_alfabeto:
                nome = nome_de_estado_lista(novo_automato[e][a])
                novo_nome = novo_automato[nome]["order"]
                estado_renomeado[a] = novo_nome
            
            automato_renomeado[nome_estado] = estado_renomeado
        r = {}
        r["alfabeto"] = novo_alfabeto
        r["automato"] = sorted(automato_renomeado.items())
        return r
        

#defini base
def get_base(simbolo = "&"):
    AutomatoBase = Automato()
    AutomatoBase.add_estado() #q1
    AutomatoBase.set_inicial(0)
    AutomatoBase.add_estado() #q2
    AutomatoBase.set_final_automato(1)
    AutomatoBase.add_transicao(0, simbolo, 1)
    return AutomatoBase

if __name__ == "__main__":
    AutomatoBase = get_base("a")
    print(AutomatoBase)
    print(AutomatoBase.alfabeto)