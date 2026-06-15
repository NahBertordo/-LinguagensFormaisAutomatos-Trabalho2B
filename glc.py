import copy


def obter_variaveis_anulaveis(rules, S, s_oculto_originalmente):
    """Passo 1 Auxiliar: Identifica variáveis anuláveis."""
    anulaveis = set()
    if s_oculto_originalmente:
        anulaveis.add(S)
    for var, producoes in rules.items():
        for prod in producoes:
            if prod == "":
                anulaveis.add(var)
    while True:
        tamanho_anterior = len(anulaveis)
        for var, producoes in rules.items():
            for prod in producoes:
                if prod != "" and all(sinal in anulaveis for sinal in prod):
                    anulaveis.add(var)
        if len(anulaveis) == tamanho_anterior:
            break
    return anulaveis


def gerar_combinacoes_vazio(cadeia, anulaveis):
    """Gera ramificações substituindo ou mantendo as variáveis anuláveis."""
    if not cadeia:
        return {""}
    primeiro = cadeia[0]
    resto = cadeia[1:]
    sufixos = gerar_combinacoes_vazio(resto, anulaveis)
    resultados = set()
    for suf in sufixos:
        resultados.add(primeiro + suf)
        if primeiro in anulaveis:
            resultados.add(suf)
    return resultados


def passo1_remover_vazios(rules, S, s_oculto_originalmente):
    """Passo 1: Elimina produções vazias, usa S como anulável mas mascara S -> eps."""
    anulaveis = obter_variaveis_anulaveis(rules, S, s_oculto_originalmente)
    novas_regras = {}
    for var, producoes in rules.items():
        subconjunto = set()
        for prod in producoes:
            if prod == "":
                continue
            combinacoes = gerar_combinacoes_vazio(prod, anulaveis)
            for c in combinacoes:
                if c != "":
                    subconjunto.add(c)
        if subconjunto:
            novas_regras[var] = list(subconjunto)
    return novas_regras


def passo2_remover_unitarias(rules, voc):
    """Passo 2: Elimina produções unitárias do tipo A -> B."""
    fechos = {v: {v} for v in voc}
    while True:
        alterado = False
        for var in voc:
            producoes = rules.get(var, [])
            for prod in producoes:
                if len(prod) == 1 and prod in voc:
                    if prod not in fechos[var]:
                        fechos[var].add(prod)
                        fechos[var].update(fechos.get(prod, set()))
                        alterado = True
        if not alterado:
            break
    novas_regras = {}
    for var in voc:
        subconjunto = set()
        for derivado in fechos[var]:
            for prod in rules.get(derivado, []):
                if not (len(prod) == 1 and prod in voc):
                    subconjunto.add(prod)
        if subconjunto:
            novas_regras[var] = list(subconjunto)
    return novas_regras


def passo3_remover_inuteis(rules, voc, terminais, S):
    """Passo 3: Remove variáveis inúteis."""
    geradores = set(terminais)
    while True:
        tamanho_anterior = len(geradores)
        for var, producoes in rules.items():
            for prod in producoes:
                if all(sinal in geradores or sinal in voc for sinal in prod):
                    geradores.add(var)
        if len(geradores) == tamanho_anterior:
            break

    regras_filtradas = {}
    for var, producoes in rules.items():
        validas = [
            p
            for p in producoes
            if all(sinal in geradores or sinal in voc for sinal in p)
        ]
        if validas:
            regras_filtradas[var] = validas

    alcancaveis = {S}
    fila = [S]
    while fila:
        atual = fila.pop(0)
        for prod in regras_filtradas.get(atual, []):
            i = 0
            while i < len(prod):
                if prod[i] == "X" and i + 1 < len(prod) and prod[i + 1].isdigit():
                    j = i + 1
                    while j < len(prod) and prod[j].isdigit():
                        j += 1
                    token = prod[i:j]
                    i = j
                else:
                    token = prod[i]
                    i += 1
                if token in voc and token not in alcancaveis:
                    alcancaveis.add(token)
                    fila.append(token)

    novas_regras = {}
    for var in alcancaveis:
        if var in regras_filtradas:
            novas_regras[var] = regras_filtradas[var]

    return novas_regras if novas_regras else rules


def separar_em_simbolos(cadeia):
    """Auxiliar para quebrar a string de produção em tokens (ex: ['X1', 'A', 'X2'])."""
    simbolos = []
    i = 0
    while i < len(cadeia):
        if cadeia[i] == "X":
            j = i + 1
            while j < len(cadeia) and cadeia[j].isdigit():
                j += 1
            simbolos.append(cadeia[i:j])
            i = j
        else:
            simbolos.append(cadeia[i])
            i += 1
    return simbolos


def tratar_tamanho_tres_esquerda(
    simbolos, mapa_intermediarias, contador_variaveis, novas_regras
):
    """Trata cadeias de exatamente 3 símbolos agrupando os dois primeiros (Esquerda)."""
    dois_primeiros = "".join(simbolos[:2])
    resto_finais = "".join(simbolos[2:])

    if dois_primeiros in mapa_intermediarias:
        nova_var_intermediaria = mapa_intermediarias[dois_primeiros]
    else:
        nova_var_intermediaria = f"X{contador_variaveis}"
        contador_variaveis += 1
        mapa_intermediarias[dois_primeiros] = nova_var_intermediaria
        novas_regras[nova_var_intermediaria] = [dois_primeiros]

    prod_fatorada = nova_var_intermediaria + resto_finais
    return prod_fatorada, contador_variaveis


def tratar_tamanho_quatro_ou_mais_direita(
    simbolos, mapa_intermediarias, contador_variaveis, novas_regras
):
    """Trata cadeias de 4 ou mais símbolos agrupando estritamente pela direita(Regra da cadeia)."""
    # Processa de forma linear e contínua até reduzir toda a cauda da cadeia
    while len(simbolos) > 2:
        duas_ultimas = "".join(simbolos[-2:])

        if duas_ultimas in mapa_intermediarias:
            nova_var = mapa_intermediarias[duas_ultimas]
        else:
            nova_var = f"X{contador_variaveis}"
            contador_variaveis += 1
            mapa_intermediarias[duas_ultimas] = nova_var
            novas_regras[nova_var] = [duas_ultimas]

        simbolos = simbolos[:-2] + [nova_var]

    return "".join(simbolos), contador_variaveis


def passo4_converter_fnc(rules, terminais, s_oculto, S):
    """Passo 4: Converte para FNC"""
    novas_regras = {}
    mapa_terminais = {}
    mapa_intermediarias = {}
    contador_variaveis = 1

    # 1. MAPEAMENTO ÚNICO DE TERMINAIS
    for t in sorted(terminais):
        nova_var = f"X{contador_variaveis}"
        contador_variaveis += 1
        mapa_terminais[t] = nova_var
        novas_regras[nova_var] = [t]

    # Substitui os terminais em todas as produções de tamanho >= 2
    regras_fase1 = {}
    for var, producoes in rules.items():
        regras_fase1[var] = []
        for prod in producoes:
            if len(prod) > 1:
                nova_prod = ""
                for sinal in prod:
                    if sinal in terminais:
                        nova_prod += mapa_terminais[sinal]
                    else:
                        nova_prod += sinal
                regras_fase1[var].append(nova_prod)
            else:
                regras_fase1[var].append(prod)

    # Inicializa o dicionário definitivo com as chaves existentes
    for k in regras_fase1.keys():
        if k not in novas_regras:
            novas_regras[k] = []

    # 2. PROCESSO DE QUEBRA ISOLADO POR CASO/EXCEÇÃO
    for var, producoes in regras_fase1.items():
        for prod in producoes:
            simbolos_validos = separar_em_simbolos(prod)
            tamanho = len(simbolos_validos)

            if tamanho == 3:
                # Exatamente 3 símbolos -> Agrupa pela ESQUERDA
                prod_fatorada, contador_variaveis = tratar_tamanho_tres_esquerda(
                    simbolos_validos,
                    mapa_intermediarias,
                    contador_variaveis,
                    novas_regras,
                )
                novas_regras[var].append(prod_fatorada)

            elif tamanho >= 4:
                # 4 ou mais símbolos -> Regra da cadeia pela DIREITA de forma isolada
                prod_fatorada, contador_variaveis = (
                    tratar_tamanho_quatro_ou_mais_direita(
                        simbolos_validos,
                        mapa_intermediarias,
                        contador_variaveis,
                        novas_regras,
                    )
                )
                novas_regras[var].append(prod_fatorada)

            else:
                # Caso base (tamanho 1 ou 2)
                novas_regras[var].append(prod)

    # Tratamento final do S Oculto
    if s_oculto:
        if S not in novas_regras:
            novas_regras[S] = []
        if "" not in novas_regras[S]:
            novas_regras[S].append("")

    return novas_regras


def separar_em_simbolos(cadeia):
    """Auxiliar para quebrar a string de produção em tokens (ex: ['X1', 'A', 'X2'])."""
    simbolos = []
    i = 0
    while i < len(cadeia):
        if cadeia[i] == "X":
            j = i + 1
            while j < len(cadeia) and cadeia[j].isdigit():
                j += 1
            simbolos.append(cadeia[i:j])
            i = j
        else:
            simbolos.append(cadeia[i])
            i += 1
    return simbolos


def tratar_tamanho_tres_esquerda(
    simbolos, mapa_intermediarias, contador_variaveis, novas_regras
):
    """Trata cadeias de exatamente 3 símbolos agrupando os dois primeiros (Esquerda)."""
    dois_primeiros = "".join(simbolos[:2])
    resto_finais = "".join(simbolos[2:])

    if dois_primeiros in mapa_intermediarias:
        nova_var_intermediaria = mapa_intermediarias[dois_primeiros]
    else:
        nova_var_intermediaria = f"X{contador_variaveis}"
        contador_variaveis += 1
        mapa_intermediarias[dois_primeiros] = nova_var_intermediaria
        novas_regras[nova_var_intermediaria] = [dois_primeiros]

    prod_fatorada = nova_var_intermediaria + resto_finais
    return prod_fatorada, contador_variaveis


def tratar_tamanho_quatro_ou_mais_direita(
    simbolos, mapa_intermediarias, contador_variaveis, novas_regras
):
    """Trata cadeias de 4 ou mais símbolos agrupando estritamente pela direita."""
    # Processa de forma linear e contínua até reduzir toda a cauda da cadeia
    while len(simbolos) > 2:
        duas_ultimas = "".join(simbolos[-2:])

        if duas_ultimas in mapa_intermediarias:
            nova_var = mapa_intermediarias[duas_ultimas]
        else:
            nova_var = f"X{contador_variaveis}"
            contador_variaveis += 1
            mapa_intermediarias[duas_ultimas] = nova_var
            novas_regras[nova_var] = [duas_ultimas]

        simbolos = simbolos[:-2] + [nova_var]

    return "".join(simbolos), contador_variaveis


def passo4_converter_fnc(rules, terminais, s_oculto, S):
    """Passo 4: Converte para FNC"""
    novas_regras = {}
    mapa_terminais = {}
    mapa_intermediarias = {}
    contador_variaveis = 1

    # 1. MAPEAMENTO ÚNICO DE TERMINAIS
    for t in sorted(terminais):
        nova_var = f"X{contador_variaveis}"
        contador_variaveis += 1
        mapa_terminais[t] = nova_var
        novas_regras[nova_var] = [t]

    # Substitui os terminais em todas as produções de tamanho >= 2
    regras_fase1 = {}
    for var, producoes in rules.items():
        regras_fase1[var] = []
        for prod in producoes:
            if len(prod) > 1:
                nova_prod = ""
                for sinal in prod:
                    if sinal in terminais:
                        nova_prod += mapa_terminais[sinal]
                    else:
                        nova_prod += sinal
                regras_fase1[var].append(nova_prod)
            else:
                regras_fase1[var].append(prod)

    # Inicializa o dicionário definitivo com as chaves existentes
    for k in regras_fase1.keys():
        if k not in novas_regras:
            novas_regras[k] = []

    # 2. PROCESSO DE QUEBRA ISOLADO POR CASO/EXCEÇÃO
    for var, producoes in regras_fase1.items():
        for prod in producoes:
            simbolos_validos = separar_em_simbolos(prod)
            tamanho = len(simbolos_validos)

            if tamanho == 3:
                # Exatamente 3 símbolos -> Agrupa pela ESQUERDA
                prod_fatorada, contador_variaveis = tratar_tamanho_tres_esquerda(
                    simbolos_validos,
                    mapa_intermediarias,
                    contador_variaveis,
                    novas_regras,
                )
                novas_regras[var].append(prod_fatorada)

            elif tamanho >= 4:
                # 4 ou mais símbolos -> Regra da cadeia pela DIREITA de forma isolada
                prod_fatorada, contador_variaveis = (
                    tratar_tamanho_quatro_ou_mais_direita(
                        simbolos_validos,
                        mapa_intermediarias,
                        contador_variaveis,
                        novas_regras,
                    )
                )
                novas_regras[var].append(prod_fatorada)

            else:
                # Caso base (tamanho 1 ou 2) permanece intocado
                novas_regras[var].append(prod)

    # Tratamento final do S Oculto
    if s_oculto:
        if S not in novas_regras:
            novas_regras[S] = []
        if "" not in novas_regras[S]:
            novas_regras[S].append("")

    return novas_regras


def formatar_estilo_antigo(rules, S):
    """Estilo inicial simples: A -> B"""

    def chave_ordenacao(var):
        if var == S:
            return (0, "")
        if var.startswith("X") and var[1:].isdigit():
            return (2, int(var[1:]))
        return (1, var)

    output = []
    chaves_ordenadas = sorted(rules.keys(), key=chave_ordenacao)
    for key in chaves_ordenadas:
        for value in sorted(rules[key]):
            exibir_valor = "eps" if value == "" else value
            output.append(f"{key} -> {exibir_valor}")
    return "\n".join(output)


def formatar_estilo_bloco(rules, S, variaveis, terminais):
    """Estilo para o arquivo de entrada/saída."""

    def chave_ordenacao(var):
        if var == S:
            return (0, "")
        if var.startswith("X") and var[1:].isdigit():
            return (2, int(var[1:]))
        return (1, var)

    todas_vars = set(variaveis) | set(rules.keys())
    vars_ordenadas = sorted(list(todas_vars), key=chave_ordenacao)

    # Identifica se o vazio (string vazia) realmente faz parte das transições ATUAIS desta etapa
    contem_vazio_real = False
    for var, prods in rules.items():
        if "" in prods:
            contem_vazio_real = True
            break

    linhas_bloco = []
    linhas_bloco.append(f"Variáveis: {' '.join(vars_ordenadas)}")

    # Só exibe "eps" na linha se ele realmente for usado nesta etapa da gramática
    lista_terminais_ordenados = sorted(list(set(terminais)))
    if contem_vazio_real:
        linhas_bloco.append(f"Terminais: {' '.join(lista_terminais_ordenados)} eps")
    else:
        linhas_bloco.append(f"Terminais: {' '.join(lista_terminais_ordenados)}")

    linhas_bloco.append(f"Simbolo inicial: {S}")
    linhas_bloco.append("Transições:")

    for key in vars_ordenadas:
        if key in rules:
            for value in sorted(rules[key]):
                exibir_valor = "eps" if value == "" else value
                linhas_bloco.append(f"{key} {exibir_valor}")

    return "\n".join(linhas_bloco)


def encontrar_derivacao(rules, S, palavra_alvo):
    if palavra_alvo == "" and "" in rules.get(S, []):
        return [("S", "eps", "")]

    fila = [(S, [])]
    visitados = set([S])

    while fila:
        atual, passos = fila.pop(0)

        if atual == palavra_alvo:
            return passos

        contagem_terminais = sum(1 for c in atual if not c.isupper())
        contagem_variaveis = sum(
            1
            for c in atual
            if c.isupper()
            and (c != "X" or (c == "X" and not atual[atual.index(c) :].isdigit()))
        )

        if len(atual) > len(palavra_alvo) * 2 + 1:
            continue

        for i, caractere in enumerate(atual):
            # Identifica se é uma variável normal (A, B, S) ou auxiliar (X1, X2)
            var_atual = ""
            proximo_indice = i + 1
            if caractere.isupper():
                if caractere == "X":
                    j = i + 1
                    while j < len(atual) and atual[j].isdigit():
                        j += 1
                    var_atual = atual[i:j]
                    proximo_indice = j
                else:
                    var_atual = caractere

            if var_atual and var_atual in rules:
                for prod in rules[var_atual]:
                    # Evita loops infinitos de substituição vazia se não for a palavra vazia
                    if prod == "" and palavra_alvo != "":
                        continue

                    nova_forma = atual[:i] + prod + atual[proximo_indice:]

                    if nova_forma not in visitados:
                        visitados.add(nova_forma)
                        passo_regragem = (
                            f"{var_atual} -> {'eps' if prod == '' else prod}"
                        )
                        novos_passos = passos + [(atual, passo_regragem, nova_forma)]
                        fila.append((nova_forma, novos_passos))
                break
    return None


def formatar_derivacao_passo_a_passo(passos, palavra):
    if passos is None:
        return f"Palavra '{palavra}': Não foi possível derivar nesta gramática.\n"

    linhas_passos = [f"Palavra: {palavra}"]
    for i, (antes, regra, depois) in enumerate(passos):
        linhas_passos.append(f"  {antes}  [Aplicar regra: {regra}]")
        if i == len(passos) - 1:
            linhas_passos.append(f"  {depois}  [Palavra gerada com sucesso!]")

    return "\n".join(linhas_passos) + "\n"
