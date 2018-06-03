VAZIO = "&"
OPERANDOS = ["|"]
OU = "|"
FIRST = dict()
FOLLOW = dict()

def get_texto(nome):
    contents = ""
    with open(nome) as f:
        for line in f.readlines():
            contents += line
    return contents

def reset_ff():
    global FIRST
    global FOLLOW
    FIRST = dict()
    FOLLOW = dict()

def uniao(a, b, exclude = []):
    for i in b:
        if i not in a and i not in exclude:
            a.append(i)
    return a

def limpa_entrada(A):
    A = A.strip()
    A = A.replace("{", "").replace("}", "")
    B = A.split(",")
    return B

def limpa_p(P):
    B = dict()
    P = P.split("\n")
    for p in P:
        p = p.strip()
        
        if len(p) < 1:
            continue
        
        p = p.split("->")
        v_index = p[0]
        B[v_index] = list()
        
        open_index = None
        close_index = None
        
        for c in range(len(p[1])):

            if p[1][c] in OPERANDOS or p[1][c] == "&":
                B[v_index].append(p[1][c])
            elif p[1][c] == "<":
                open_index = c
            elif p[1][c] == ">":
                close_index = c
            
            if open_index is not None and close_index is not None:
                B[v_index].append(p[1][open_index:close_index+1])
                open_index = None
                close_index = None
    return B

def get_regras(P):
    r = list()
    a_index = None
    
    for p in range(len(P)):
        if a_index is None:
            a_index = p
        elif a_index is not None and P[p] == OU:
            r.append((a_index, p-1))
            a_index = None
    if a_index is not None:
        r.append((a_index, len(P)-1))
    return r

def first(A, V, T, P):
    
    if A not in V:
        return ["&"]

    global FIRST
    
    if A in FIRST:
        return FIRST[A]
    
    conjunto = list()
    
    ativar_index = True
    for index in range(len(P[A])):
        
        if ativar_index:
            ativar_index = False
            primeiro = P[A][index]
        
            if primeiro == "&":
                conjunto = uniao(conjunto, ["&"])
            if primeiro in T:
                conjunto = uniao(conjunto, [primeiro])
            if primeiro in V:
                first_primeiro = first(primeiro, V, T, P)
                if VAZIO in first_primeiro:
                    ativar_index
                conjunto = uniao(conjunto, first_primeiro)
        if P[A][index] == OU:
            ativar_index = True
    
    FIRST[A] = conjunto
    return FIRST[A]

def follow(A, V, T, P, S):
    global FIRST
    global FOLLOW

    if A in FOLLOW:
        return FOLLOW[A]
    
    conjunto = list()

    for p in P:
        if A not in P[p]:
            continue
        
        follow_p_added = False
        regras = get_regras(P[p])
        
        for regra in regras:
            ativar_rhs = False
            proximo_first = False
            for index in range(regra[0], regra[1]+1):
                
                if ativar_rhs:
                    if P[p][index] in T and not proximo_first:
                        conjunto.append(P[p][index])

                    if P[p][index] in V:
                        first_index = FIRST[P[p][index]][:]
                        proximo_first = False
                        ativar_rhs = False
                        if "&" in first_index:
                            ativar_rhs = True
                            proximo_first = True
                            first_index.remove("&")

                        conjunto = uniao(conjunto, first_index)

                        if proximo_first and index == regra[1] and p != A:
                            proximo_first = False
                            conjunto = uniao(conjunto, follow(p, V, T, P, S))
                            follow_p_added = True

                        
                if P[p][index] == A:
                    ativar_rhs = True
        
        if not follow_p_added and p != A:
            for regra in regras:
                if A == P[p][regra[1]]:
                    conjunto = uniao(conjunto, follow(p, V, T, P, S))
                        

    if A == S and "$" not in conjunto:
        conjunto.append("$")
    
    FOLLOW[A] = conjunto
    return FOLLOW[A]


def first_follow():
    
    reset_ff()
    S = "<E>"
    V = limpa_entrada(get_texto("LL1/V.txt").strip("\n"))
    T = limpa_entrada(get_texto("LL1/T.txt").strip("\n"))
    P = limpa_p(get_texto("LL1/P.txt"))
    
    print("V:", V)
    print("T:", T)
    print("P:")
    for p in P:
        print(p, "->", P[p])

    for v in V:
        first(v, V, T, P)
    
    for v in V:
        follow(v, V, T, P, S)
    
    print("")
    print("*"*20)
    print("First:")
    for f in FIRST:
        print(f, "=", FIRST[f])

    print("")
    print("*"*20)
    print("FOLLOW:")
    for f in FOLLOW:
        print(f, "=", FOLLOW[f])

def tabela_sintatica():
    S = "<E>"
    V = limpa_entrada(get_texto("LL1/V.txt").strip("\n"))
    T = limpa_entrada(get_texto("LL1/T.txt").strip("\n"))
    P = limpa_p(get_texto("LL1/P.txt"))
    
    tabela = dict()
    
    for p in P:
        tabela[p] = dict()
        for t in T:
            tabela[p][t] = None
        tabela[p]["$"] = None
    
    for p in P:
        regras = get_regras(P[p])
        for regra in regras:
            f = first(p, V, T, P)
            fw = follow(p, V, T, P, S)
            # slice não inclui a ultima posição
            r = P[p][regra[0]:regra[1]+1]
            print("RR:", r)
            #regra 1
            if P[p][regra[0]] in T:
                tabela[p][P[p][regra[0]]] = r
            else:
                #regra 2.i
                if "&" not in f:
                    for a in f:
                        tabela[p][a] = r
                else:
                    first_all = first(P[p][regra[0]], V, T, P)
                    #regra 2.ii
                    print("vazio a:", r, "fall:", first_all)
                    if "&" in first_all:
                        first_all = uniao(first_all, fw)
                        first_all.remove("&")
                    print("vazio b:", r, "fall:", first_all)
                    for a in first_all:
                        tabela[p][a] = r
                    #regra 2.iii
                    if "$" in fw:
                        tabela[p]["$"] = r
    print("*"*20)
    print("Tabela")
    for t in tabela:
        print(t, tabela[t])



if __name__ == "__main__":
    first_follow()
    tabela_sintatica()