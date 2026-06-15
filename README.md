Linguagens Formais e Autômatos
Linguagem: Python

1) Parte 1: Limpeza da gramática:
  Podem-se remover todas as produções indesejáveis através da seguinte sequência de passos:
  1º - Remover as produções-vazias
  2º - Remover as produções-unidade
  3º - Remover as produções inúteis.

2) Parte 2: Converter para forma normal de Chomsky ou Greibach

3) Estrutura do arquivo de entrada e saída.
  Procedimento:
  Entrada: arquivo txt
  Variáveis: S A B C D E
  Terminais: a b c d e eps
  Simbolo inicial: S
  Transições:
  S aA
  S eps
  A bBaA
  A eps
  A palavra vazia será simbolizada por: eps
  Na regra (S aA) o espaço entre S e a significa a -> a seta da transição. Então este espaço
  precisa existir.
  Parte 1:
  -Gerar a gramática limpa. Exibir a gramática limpa no formato do arquivo de entrada.
  Parte 2:
  -Com a gramática limpa da parte 1 (entrada), converter a gramática para forma normal de
  Chomsky ou Greibach.
  -Exibir a gramática na forma normal de Chomsky ou Greibach no formato do arquivo de
  entrada.
-Parte 3:
  Testar a gramática na forma Normal gerada na parte 2 com um conjunto de palavras
  (terminais): estas palavras devem ser as mesmas que são reconhecidas pela gramática de
  entrada que ainda não foi limpa.
  O teste implica em gerar a palavra dada passo a passo: mostrar a palavra e qual regra será
  aplicada. Assim na próxima linha exibe a palavra com a substituição já feita e a próxima
  regra a ser aplicada. Fazer isso sucessivamente até gerar a palavra.  
