class Automato(object):
    alfabeto = []
    estados = {}
    estado_inicial = None
    estado_final = None
    estados_finais = []

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
    
    def __len__(self):
        return len(self.estados)

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
                novas_opcoes[opt] = self.estados[estado][opt] + offset
        
        novas_opcoes["inicial"] = self.estados[estado]["inicial"]
        novas_opcoes["final"] = self.estados[estado]["final"]
        return novas_opcoes

    
    def add_transicao(self, estado_entrada, simbolo, estado_saida):

        if simbolo not in self.alfabeto:
            self.alfabeto.append(simbolo)

        if estado_entrada in self.estados and estado_saida in self.estados:
            self.estados[estado_entrada][simbolo] = estado_saida
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
                for estado_final in self.estados_finais:
                    if estado == estado_final:
                        del self.estados_finais[estado] 
                self.estados[estado]["final"] = False
                return True
            
            self.estados_finais.append(estado)
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
def get_base(simbolo):
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