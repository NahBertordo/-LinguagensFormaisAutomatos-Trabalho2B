# Linguagens Formais e Autômatos — Manipulador de Gramáticas Livres de Contexto

Este projeto em **Python** realiza a limpeza de Gramáticas Livres de Contexto (GLC), conversão para a Forma Normal de Chomsky (FNC) e testes de derivação passo a passo de palavras.

---

## 🛠️ Funcionamento do Projeto

O programa é dividido estritamente em três etapas fundamentais:

### 1️⃣ Parte 1: Limpeza da Gramática
Remove todas as produções indesejáveis da gramática de entrada seguindo rigorosamente a sequência padrão:
* **1º Passo:** Remoção de produções vazias (`eps`).
* **2º Passo:** Remoção de produções unitárias (regras do tipo $A \rightarrow B$).
* **3º Passo:** Remoção de produções inúteis (símbolos não-geradores ou inalcançáveis).

### 2️⃣ Parte 2: Conversão para a Forma Normal de Chomsky
Pega o resultado limpo da *Parte 1* e o converte para o formato padrão da FNC, onde todas as regras assumem estritamente as formas:
* $A \rightarrow BC$ (Variável gerando duas variáveis)
* $A \rightarrow a$ (Variável gerando um terminal)

### 3️⃣ Parte 3: Testador de Palavras e Derivação Passo a Passo
Recebe uma lista de palavras formadas por caracteres terminais para validar se pertencem à linguagem da gramática.
* Reconstrói e imprime na tela a **derivação linha por linha**, mostrando qual variável está sendo substituída por qual regra até formar a string desejada.

---

## 📂 Estrutura de Arquivos (Entrada e Saída)

As gramáticas de entrada e saída utilizam espaçamentos simples como delimitadores. O espaço em branco após o cabeçalho da regra indica a seta da transição ($\rightarrow$).

### Exemplo de Entrada (`entrada.txt`)
```text
S A B C D E      *Variáveis
a b c d e eps    *Terminais
S                *Simbolo inicial
S aA             *Começo das Transições
S eps
A bBaA
A eps
```
---
