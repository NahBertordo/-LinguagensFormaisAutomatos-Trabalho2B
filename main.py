"""
                    TRABALHO 2° BIMESTRE DE LINGUAGENS FORMAIS E AUTÔMATOS
Objetivo: SIMPLIFICAÇÃO, CONVERSÃO PARA FORMA NORMAL DE CHOMSKY E TESTE DE GRAMÁTICA NA FNC E NA ORIGINAL
---------------------------------------------------------------------------------
Este códigé dividido em 3 partes:
1° parte: Limpeza da gramática
2° parte: Converter para forma normal de Chomsky
3° parte: Testar a gramática na forma Normal e na original
"""

import copy
from glc import (
    passo1_remover_vazios,
    passo2_remover_unitarias,
    passo3_remover_inuteis,
    passo4_converter_fnc,
    formatar_estilo_antigo,
    formatar_estilo_bloco,
    encontrar_derivacao,
    formatar_derivacao_passo_a_passo,
)


def main():
    # -------------------------------------------------------------------------
    #           LEITURA E TRATAMENTO DA GRAMÁTICA DE ENTRADA
    # -------------------------------------------------------------------------
    try:
        with open("entrada.txt", "r", encoding="utf-8") as f:
            linhas_brutas = [
                linha.strip() for open_line in f if (linha := open_line.strip())
            ]
    except FileNotFoundError:
        print("Erro: O arquivo 'entrada.txt' não foi encontrado.")
        return

    linhas = []
    for l in list(linhas_brutas):
        if "*" in l:
            l = l.split("*")[0].strip()
        else:
            l = l.strip()
        if l:
            linhas.append(l)

    # Identificação posicional da estrutura da gramática
    variaveis = linhas[0].split()
    terminais = linhas[1].split()
    if "eps" in terminais:
        terminais.remove("eps")
    S = linhas[2].strip()

    transicoes_brutas = linhas[3:]
    rules = {}
    s_oculto_detectado = False

    for transicao in transicoes_brutas:
        partes = transicao.split()
        if len(partes) == 2:
            fr, to = partes[0], partes[1]
            if to == "eps":
                to = ""
                if fr == S:
                    s_oculto_detectado = True
                    continue
            rules.setdefault(fr, []).append(to)

    gramatica_original_pura = copy.deepcopy(rules)
    if s_oculto_detectado:
        gramatica_original_pura.setdefault(S, []).append("")

    # -------------------------------------------------------------------------
    #           LEITURA DAS PALAVRAS DE TESTE
    # -------------------------------------------------------------------------
    palavras_teste = []
    try:
        with open("palavras.txt", "r", encoding="utf-8") as f_palavras:
            conteudo_palavras = f_palavras.read()
            linhas_p_brutas = [
                p.strip() for p in conteudo_palavras.split() if p.strip()
            ]
            for p in linhas_p_brutas:
                if "*" in p:
                    p = p.split("*")[0].strip()
                if p:
                    palavras_teste.append(p)
    except FileNotFoundError:
        print(
            "Aviso: O arquivo 'palavras.txt' não foi encontrado. A Parte 3 será pulada."
        )

    resultado = []

    # -------------------------------------------------------------------------
    #           EXECUÇÃO DOS PASSOS DE SIMPLIFICAÇÃO
    # -------------------------------------------------------------------------
    resultado.append("=== GRAMÁTICA ORIGINAL ===")
    resultado.append(
        formatar_estilo_bloco(gramatica_original_pura, S, variaveis, terminais) + "\n"
    )

    # Passo 1: Remover produções vazias
    rules = passo1_remover_vazios(rules, S, s_oculto_detectado)
    resultado.append("=== PASSO 1: APÓS REMOÇÃO DE REGRAS VAZIAS ===")
    resultado.append(formatar_estilo_antigo(rules, S) + "\n")

    # Passo 2: Remover produções unitárias
    rules = passo2_remover_unitarias(rules, variaveis)
    resultado.append("=== PASSO 2: APÓS REMOÇÃO DE REGRAS UNITÁRIAS ===")
    resultado.append(formatar_estilo_antigo(rules, S) + "\n")

    # Passo 3: Remover variáveis inúteis
    rules = passo3_remover_inuteis(rules, variaveis, terminais, S)
    resultado.append("=== PASSO 3: APÓS REMOÇÃO DE VARIÁVEIS INÚTEIS ===")
    resultado.append(formatar_estilo_antigo(rules, S) + "\n")

    # Exibição da Gramática Limpa / Simplificada
    regras_exibicao_limpa = copy.deepcopy(rules)
    if s_oculto_detectado:
        regras_exibicao_limpa.setdefault(S, []).append("")
    variaveis_limpas = [v for v in variaveis if v in regras_exibicao_limpa]
    if S not in variaveis_limpas and S in regras_exibicao_limpa:
        variaveis_limpas.insert(0, S)

    resultado.append("=== GRAMÁTICA LIMPA ===")
    resultado.append(
        formatar_estilo_bloco(regras_exibicao_limpa, S, variaveis_limpas, terminais)
        + "\n"
    )

    # Passo 4: Converter para FNC (Forma Normal de Chomsky Final)
    rules_chomsky = passo4_converter_fnc(rules, terminais, s_oculto_detectado, S)
    resultado.append("=== PASSO 4: FORMA NORMAL DE CHOMSKY FINAL ===")
    resultado.append(
        formatar_estilo_bloco(rules_chomsky, S, variaveis, terminais) + "\n"
    )

    # -------------------------------------------------------------------------
    #     TESTE DE DERIVAÇÃO DAS PALAVRAS - COMPARATIVO (ORIGINAL VS CHOMSKY)
    # -------------------------------------------------------------------------
    resultado.append("=== PARTE 3: DERIVAÇÃO DE PALAVRAS PASSO A PASSO ===")
    if not palavras_teste:
        resultado.append(
            "Nenhuma palavra válida foi fornecida no arquivo 'palavras.txt'.\n"
        )
    else:
        for palavra in palavras_teste:
            palavra_processada = "" if palavra == "eps" else palavra
            resultado.append(
                f"--------------------------------------------------\nPALAVRA TESTADA: '{palavra}'\n--------------------------------------------------"
            )

            # TESTE A: Derivação utilizando a Gramática de Entrada (Original)
            resultado.append("A) DERIVAÇÃO NA GRAMÁTICA ORIGINAL:")
            passos_original = encontrar_derivacao(
                gramatica_original_pura, S, palavra_processada
            )
            resultado.append(formatar_derivacao_passo_a_passo(passos_original, palavra))

            # TESTE B: Derivação utilizando a Forma Normal de Chomsky (FNC Final)
            resultado.append("B) DERIVAÇÃO NA FORMA NORMAL DE CHOMSKY:")
            passos_chomsky = encontrar_derivacao(rules_chomsky, S, palavra_processada)
            resultado.append(
                formatar_derivacao_passo_a_passo(passos_chomsky, palavra) + "\n"
            )

    # -------------------------------------------------------------------------
    #       SALVAMENTO DO ARQUIVO FINAL
    # -------------------------------------------------------------------------
    with open("saida.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(resultado))

    print("Processamento concluído com sucesso! Verifique o arquivo 'saida.txt'.")


if __name__ == "__main__":
    main()
