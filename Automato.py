class Automato(object):
    alfabeto = None
    estados = None
    estado_inicial = None
    estado_final = None

    def __init__(self):
        self.alfabeto = list()
        self.estados = dict()
    
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