class Automato():
    alfabeto = []
    estados = {}
    estado_inicial = None
    estado_final = None

    def __init__(self):
        pass
    
    def __str__(self):
        return_str = ""
        for estado in self.estados:
            
            return_str += "q{0}:".format(estado)
            
            for ops in self.estados[estado]:
                return_str += "({0}:{1})".format(ops, self.estados[estado][ops])
            return_str += "\n"

        return return_str

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
    
    def add_transicao(self, estado_entrada, simbolo, estado_saida):

        if simbolo not in self.alfabeto:
            self.alfabeto.append(simbolo)

        if estado_entrada in self.estados and estado_saida in self.estados:
            self.estados[estado_entrada][simbolo] = estado_saida
            return True
        else:
            return False

    def set_inicial(self, estado):
        if estado in self.estados:
            if self.estado_inicial is not None: 
                self.estados[self.estado_inicial]["inicial"] = False
            self.estado_inicial = estado
            self.estados[estado]["inicial"] = True
            return True
        else:
            return False
    
    def set_final(self, estado):
        if estado in self.estados:
            self.estados[estado]["final"] = True
            return True
        else:
            return False


    def set_final_automato(self, estado):
        if self.set_final(estado):
            self.estado_final = estado
        else:
            return False

#defini base
Base = Automato()
Base.add_estado() #q1
Base.set_inicial(0)
Base.add_estado() #q2
Base.set_final_automato(1)
Base.add_transicao(0, "&", 1)
Base.add_transicao(0, "a", 1)
Base.add_transicao(0, "b", 1)

def unicao(automado_a, automado_b):
    pass

def concatenacao(automato_a, automato_b):
    pass

if __name__ == "__main__":
    print(Base)
    print(Base.alfabeto)