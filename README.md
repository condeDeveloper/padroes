# Permutações que evitam um padrão

Uma permutação **contém** o padrão `p` quando tem uma subsequência — não
necessariamente seguida — na mesma ordem relativa que `p`. A permutação
`3 1 4 2` contém o padrão `2 1 3`, porque `3 1 4` sobe depois de descer do mesmo
jeito. Quem não contém, **evita**.

A pergunta é quantas permutações de tamanho `n` evitam cada padrão. Para padrão
de tamanho 3, Knuth respondeu em 1968: os seis dão Catalan. Para tamanho 4 a
conta se parte, e um dos vinte e quatro — o `1324` — não tem fórmula até hoje.

Este repositório não usa nenhuma fórmula. Ele conta, e deixa que as coincidências
apareçam sozinhas.

Python puro, sem dependência. 25 testes.

```bash
pip install -e ".[dev]"
python -m pytest
python -m padroes contar 1324 9
python -m padroes orbitas 4
python -m padroes wilf
python ferramentas/medidor.py --tudo
```

## Contar crescendo, não peneirando

Peneirar é o caminho óbvio: abrir as `n!` permutações e perguntar a cada uma. Não
serve, porque as que evitam são muito menos que `n!` — na ordem 10, as que
evitam `1234` são **586.590** de 3.628.800, **16,16%**.

O caminho aqui cresce. Se uma permutação evita o padrão, apagar o maior valor
dela também evita: tirar elemento nunca cria subsequência. Então toda evitante
de tamanho `n` sai de uma evitante de tamanho `n-1` com o valor `n` inserido em
alguma posição. Basta gerar essas `n` inserções e testar.

Os dois caminhos foram conferidos um contra o outro até a ordem 8, e os dois
testes de "contém" — o que abre todas as `C(n,k)` subsequências e o que casa o
padrão posição por posição com poda — não discordam em nenhuma das 5.040
permutações da ordem 7.

## Tamanho 3: Catalan, seis vezes

| padrão | contagens até a ordem 9 |
|---|---|
| 123, 132, 213, 231, 312, 321 | 1, 2, 5, 14, 42, 132, 429, 1.430, 4.862 |
| Catalan | 1, 2, 5, 14, 42, 132, 429, 1.430, 4.862 |

As simetrias — inverter, ler de trás para frente, virar de cabeça para baixo —
agrupam os seis em **duas** órbitas, de tamanhos 2 e 4. Que as duas deem o mesmo
número **não** é simetria: é o teorema.

## Tamanho 4: sete órbitas, três respostas

| representante | padrões na órbita | contagens até a ordem 9 |
|---|---:|---|
| 1234 | 2 | 1, 2, 6, 23, 103, **513**, 2.761, 15.767, 94.359 |
| 1243 | 4 | 1, 2, 6, 23, 103, **513**, 2.761, 15.767, 94.359 |
| 1432 | 4 | 1, 2, 6, 23, 103, **513**, 2.761, 15.767, 94.359 |
| 2143 | 2 | 1, 2, 6, 23, 103, **513**, 2.761, 15.767, 94.359 |
| 1324 | 2 | 1, 2, 6, 23, 103, **513**, 2.762, 15.793, 94.776 |
| 1342 | 8 | 1, 2, 6, 23, 103, **512**, 2.740, 15.485, 91.245 |
| 2413 | 2 | 1, 2, 6, 23, 103, **512**, 2.740, 15.485, 91.245 |

Sete órbitas de simetria, **três** sequências. As coincidências entre órbitas
diferentes não são explicadas por simetria nenhuma, e são exatamente o assunto do
campo: cada uma delas foi um artigo.

| classe | padrões | órbitas | ordem 10 |
|---|---:|---:|---:|
| 1342, 2413 | 10 | 2 | 555.662 |
| 1234, 1243, 1432, 2143 | 12 | 4 | 586.590 |
| 1324 | 2 | 1 | 591.950 |

## Quatro achados

**1. Vinte e quatro padrões, sete órbitas de simetria, e só três respostas.** As
simetrias explicam por que padrões da mesma órbita contam igual — isso vale sem
teorema. O que elas **não** explicam é por que quatro órbitas distintas (12
padrões) dão exatamente a mesma sequência, nem por que `1342` e `2413` coincidem.
A varredura encontra as três classes sem saber que elas existem.

**2. Até a ordem 5 os vinte e quatro padrões são indistinguíveis.** Todos dão
`1, 2, 6, 23, 103`. A primeira separação é na ordem **6**, e é de **um**: 512
contra 513. E `1324` só se separa de `1234` na ordem **7**, por **um** também:
2.762 contra 2.761. Quem parasse na ordem 6 concluiria que existem duas classes;
quem parasse na 5, que existe uma.

**3. A diferença entre as classes é minúscula onde ela nasce e grande onde ela
cresce.** Na ordem 7, `1324` tem **1** permutação a mais que `1234`; na ordem 9,
tem **417**; na ordem 10, **5.360**. E a classe do `1342`, que é a menor, fica
**6,13%** abaixo da do `1324` na ordem 10. A ordem entre as três — `1342` menor,
`1234` no meio, `1324` maior — se mantém em todas as ordens a partir da sétima.

**4. Evitar um padrão de quatro é comum, e deixa de ser.** Na ordem 5, **85,83%**
das permutações evitam `1234`; na ordem 10, **16,16%**. A fração desaba enquanto
o número absoluto sobe de 103 para 586.590.

## O que as medidas me corrigiram

- **Errei duas razões de cabeça neste mesmo README.** Escrevi 16,1655 onde o
  programa deu 16,1648, e 6,53% onde ele deu 6,13%. As duas eram divisões que eu
  "já sabia" o resultado. A primeira o teste pegou; a segunda eu só peguei
  porque fui recalcular todas antes de fechar. A regra já era essa, e eu a
  quebrei duas vezes na mesma página: **todo número derivado passa pelo programa
  antes de entrar no arquivo.**
- **Eu achei que simetria explicasse as coincidências.** Explica algumas: as
  órbitas existem por isso. Mas quatro órbitas distintas dão a mesma sequência, e
  nenhuma composição de inverso, reverso e complemento leva `1234` em `1243`. Só
  percebi isso quando separei as duas tabelas — a de órbitas e a de contagens —
  e elas não bateram.
- **Eu ia parar na ordem 6.** Daria duas classes, não três: `1324` e `1234`
  coincidem até a sexta. A terceira classe aparece na sétima, por uma
  permutação de diferença. Parar cedo não dá resposta aproximada: dá resposta
  errada.
- **A primeira versão peneirava as `n!` permutações.** Na ordem 9 são 362.880 por
  padrão e eu precisava de 24 padrões. Crescer a partir da ordem anterior usa o
  fato de que apagar o maior valor não cria subsequência — é uma linha de
  raciocínio, não uma otimização de código, e foi o que fez a ordem 10 caber.
- **Eu esperava que o teste com poda e o teste na marra divergissem em algum
  caso de borda** (padrão maior que a permutação, permutação de tamanho 1,
  padrão repetido). Não divergem em nenhuma das 5.040 permutações da ordem 7, com
  padrão de tamanho 3 e de tamanho 4. O caso de borda que eu procurava era o
  padrão maior que a permutação, e os dois respondem "não contém" pelo mesmo
  motivo: não há subsequência do tamanho pedido.

## Arquivos

```
padroes/nucleo.py     conter um padrão, por dois caminhos, e as simetrias
padroes/varredura.py  conta as evitantes de cada ordem, crescendo da anterior
padroes/juiz.py       Catalan, simetria e as bordas, cobrados da contagem
padroes/medidas.py    as tabelas deste README
ferramentas/medidor.py
testes/               25 testes, os pesados separados
```

O `juiz.py` não sabe contar evitantes: ele sabe o que o resultado tem de
obedecer.
