# -*- coding: utf-8 -*-
"""As tabelas do README, calculadas aqui e em lugar nenhum mais.

Nenhum numero deste projeto foi digitado a mao: o `ferramentas/medidor.py`
imprime o que sai daqui, e os testes prendem os mesmos valores.

Contar ate a ordem 10 custa quase vinte segundos por padrao, entao cada
`(padrao, ate)` fica guardado.
"""
from __future__ import annotations

from math import factorial

from .juiz import (as_orbitas_cobrem_tudo, catalanos, classes_de_wilf,
                   primeira_ordem_que_separa, tamanho_das_orbitas)
from .nucleo import orbitas, todos_os_padroes
from .varredura import contagens

_cache: dict[tuple, list[int]] = {}


def serie(padrao, ate: int) -> list[int]:
    chave = (tuple(padrao), ate)
    if chave not in _cache:
        _cache[chave] = contagens(ate, padrao)
    return _cache[chave]


def tabela_tamanho_3(ate: int = 9):
    """`(padrao, contagens, bate_com_catalan)` para os seis padroes de tamanho 3."""
    alvo = catalanos(ate)
    return [(p, serie(p, ate), serie(p, ate) == alvo) for p in todos_os_padroes(3)]


def tabela_orbitas(k: int = 4):
    """`(representante, tamanho_da_orbita, contagens)`, uma linha por orbita."""
    return [(g[0], len(g), serie(g[0], 9)) for g in orbitas(k)]


def tabela_wilf(k: int = 4, ate: int = 9):
    """As classes de contagem, com quantos padroes e quantas orbitas cada uma.

    `(contagens, quantos_padroes, quantas_orbitas, representantes)`.
    """
    por_padrao = {}
    for grupo in orbitas(k):
        c = serie(grupo[0], ate)
        for p in grupo:
            por_padrao[p] = c
    saida = []
    for classe in classes_de_wilf(por_padrao):
        c = por_padrao[classe[0]]
        quantas = sum(1 for g in orbitas(k) if g[0] in classe)
        saida.append((c, len(classe), quantas, sorted(
            g[0] for g in orbitas(k) if g[0] in classe)))
    return saida


def tabela_separacao(ate: int = 9):
    """Em que ordem cada par de classes de tamanho 4 comeca a divergir.

    `(representante_a, representante_b, primeira_ordem)`.
    """
    classes = tabela_wilf(4, ate)
    saida = []
    for i in range(len(classes)):
        for j in range(i + 1, len(classes)):
            a, b = classes[i], classes[j]
            saida.append((a[3][0], b[3][0],
                          primeira_ordem_que_separa(a[0], b[0])))
    return saida


def tabela_fracao(padroes=((1, 2, 3), (1, 2, 3, 4)), ate: int = 9):
    """Que fracao das n! permutacoes evita cada padrao: `(padrao, n, quantas, n!)`."""
    linhas = []
    for p in padroes:
        c = serie(p, ate)
        for n, quantas in enumerate(c, start=1):
            linhas.append((tuple(p), n, quantas, factorial(n)))
    return linhas


def resumo_das_orbitas(k: int = 4):
    """`(quantas_orbitas, tamanhos, cobrem_tudo)`."""
    return (len(orbitas(k)), tamanho_das_orbitas(k), as_orbitas_cobrem_tudo(k))
