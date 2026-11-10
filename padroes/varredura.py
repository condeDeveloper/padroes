# -*- coding: utf-8 -*-
"""Conta as permutacoes que evitam um padrao, crescendo em vez de peneirar.

Peneirar e o caminho obvio: abrir as n! permutacoes e perguntar a cada uma. Nao
serve, porque as que evitam sao MUITO menos que n!: na ordem 10 sao 16.796 de
3.628.800 para padrao de tamanho 3, uma em duzentas e dezesseis.

O caminho aqui cresce. Se uma permutacao evita o padrao, apagar o maior valor
dela tambem evita -- tirar elemento nunca cria subsequencia. Entao toda evitante
de tamanho n sai de uma evitante de tamanho n-1, inserindo o valor n em alguma
das n posicoes. Basta gerar essas n insercoes e testar cada uma.

A lista de uma ordem nasce da lista da ordem anterior, e nenhuma permutacao que
contem o padrao e aberta duas vezes.
"""
from __future__ import annotations

from itertools import permutations

from .nucleo import contem, contem_na_marra


class Rodada:
    """O que a contagem de uma ordem devolve."""

    def __init__(self, n: int, padrao):
        self.n = n
        self.padrao = tuple(padrao)
        self.evitantes: list[tuple[int, ...]] = []
        self.testes = 0

    @property
    def quantas(self) -> int:
        return len(self.evitantes)

    def __repr__(self) -> str:
        return ("Rodada(n=%d, padrao=%s, evitantes=%d)"
                % (self.n, "".join(str(v) for v in self.padrao), self.quantas))


def crescer(ate: int, padrao) -> list[Rodada]:
    """As rodadas de 1 ate `ate`, cada uma crescida da anterior."""
    padrao = tuple(padrao)
    rodadas = []
    anterior: list[tuple[int, ...]] = [()]
    for n in range(1, ate + 1):
        r = Rodada(n, padrao)
        for base in anterior:
            for posicao in range(n):
                nova = base[:posicao] + (n,) + base[posicao:]
                r.testes += 1
                if not contem(nova, padrao):
                    r.evitantes.append(nova)
        rodadas.append(r)
        anterior = r.evitantes
    return rodadas


def contar(n: int, padrao) -> int:
    """Quantas permutacoes de tamanho n evitam o padrao."""
    if n < 1:
        raise ValueError("a permutacao comeca em 1")
    return crescer(n, padrao)[-1].quantas


def contar_peneirando(n: int, padrao) -> int:
    """O caminho obvio: abre as n! permutacoes. Existe para julgar o de cima."""
    total = 0
    for p in permutations(range(1, n + 1)):
        if not contem(p, padrao):
            total += 1
    return total


def desacordos_entre_os_dois_testes(n: int, padrao) -> int:
    """Quantas das n! permutacoes recebem respostas diferentes dos dois testes."""
    ruins = 0
    for p in permutations(range(1, n + 1)):
        if contem(p, padrao) != contem_na_marra(p, padrao):
            ruins += 1
    return ruins


def contagens(ate: int, padrao) -> list[int]:
    """A sequencia de contagens, de 1 ate `ate`."""
    return [r.quantas for r in crescer(ate, padrao)]
