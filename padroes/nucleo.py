# -*- coding: utf-8 -*-
"""Padroes em permutacoes: o que e conter um, e como se confere.

Uma permutacao **contem** o padrao `p` quando ela tem uma subsequencia, nao
necessariamente seguida, cujos elementos ficam na mesma ordem relativa que os de
`p`. A permutacao `3 1 4 2` contem o padrao `2 1 3`, porque `3 1 4` sobe depois
de descer do mesmo jeito. Quem nao contem, **evita**.

Isso e o assunto inteiro: contar quantas permutacoes de tamanho n evitam cada
padrao. Para padrao de tamanho 3, Knuth respondeu em 1968 e a resposta e Catalan
para os seis. Para tamanho 4 a conta se divide, e um dos vinte e quatro padroes,
o `1 3 2 4`, nao tem formula ate hoje.

Duas implementacoes decidem "contem?", e elas nao compartilham uma linha:

    `contem_na_marra`  abre todas as C(n,k) subsequencias e compara;
    `contem`           casa o padrao posicao por posicao, com poda.

A segunda e a que a varredura usa; a primeira existe para julga-la.
"""
from __future__ import annotations

from itertools import combinations, permutations


def padrao_de(valores) -> tuple[int, ...]:
    """A forma de uma sequencia: trocar cada valor pelo seu posto, de 1 em diante.

    `(30, 10, 40)` vira `(2, 1, 3)`. E so isso que importa num padrao: a ordem
    relativa, nunca os valores.
    """
    ordenados = sorted(valores)
    posto = {v: i + 1 for i, v in enumerate(ordenados)}
    return tuple(posto[v] for v in valores)


def contem_na_marra(perm, padrao) -> bool:
    """Abre todas as subsequencias do tamanho do padrao e compara a forma."""
    k = len(padrao)
    alvo = tuple(padrao)
    for sub in combinations(perm, k):
        if padrao_de(sub) == alvo:
            return True
    return False


def contem(perm, padrao) -> bool:
    """Casa o padrao posicao por posicao, com poda.

    Vai escolhendo qual elemento da permutacao faz o papel de cada posicao do
    padrao, em ordem. A poda: o candidato tem de respeitar, com TODOS os ja
    escolhidos, a mesma relacao de maior ou menor que o padrao manda. Assim que
    uma relacao quebra, o ramo morre -- e nao se abre o resto da subsequencia.
    """
    n, k = len(perm), len(padrao)
    if k > n:
        return False
    escolhidos: list[int] = []

    def passo(i: int, desde: int) -> bool:
        if i == k:
            return True
        # Nao adianta comecar depois do ponto em que ja nao cabem os que faltam.
        for j in range(desde, n - (k - i) + 1):
            valor = perm[j]
            bom = True
            for a in range(i):
                antes = padrao[a] < padrao[i]
                if (escolhidos[a] < valor) != antes:
                    bom = False
                    break
            if not bom:
                continue
            escolhidos.append(valor)
            if passo(i + 1, j + 1):
                escolhidos.pop()
                return True
            escolhidos.pop()
        return False

    return passo(0, 0)


def evita(perm, padrao) -> bool:
    return not contem(perm, padrao)


def inverso(p) -> tuple[int, ...]:
    """A permutacao inversa: onde cada valor estava."""
    saida = [0] * len(p)
    for posicao, valor in enumerate(p):
        saida[valor - 1] = posicao + 1
    return tuple(saida)


def reverso(p) -> tuple[int, ...]:
    """Ler de tras para frente."""
    return tuple(reversed(p))


def complemento(p) -> tuple[int, ...]:
    """Trocar cada valor por n+1 menos ele: virar de cabeca para baixo."""
    n = len(p)
    return tuple(n + 1 - v for v in p)


def simetrias(p) -> set:
    """As oito imagens do padrao pelo grupo gerado por inverso, reverso e complemento.

    Esse grupo age no quadrado do diagrama da permutacao do mesmo jeito que o
    grupo do quadrado age num quadrado: sao as mesmas oito simetrias. Dois
    padroes na mesma orbita sao contados IGUAL em toda ordem, e isso nao e
    conjetura: e consequencia de a simetria levar subsequencia em subsequencia.
    """
    atual = {tuple(p)}
    while True:
        novos = set(atual)
        for q in atual:
            novos.add(inverso(q))
            novos.add(reverso(q))
            novos.add(complemento(q))
        if novos == atual:
            return atual
        atual = novos


def todos_os_padroes(k: int) -> list[tuple[int, ...]]:
    return [tuple(p) for p in permutations(range(1, k + 1))]


def orbitas(k: int) -> list[list[tuple[int, ...]]]:
    """Os padroes de tamanho k agrupados pelas oito simetrias, em ordem."""
    vistos: set = set()
    saida = []
    for p in todos_os_padroes(k):
        if p in vistos:
            continue
        grupo = sorted(simetrias(p))
        vistos.update(grupo)
        saida.append(grupo)
    return saida
