# -*- coding: utf-8 -*-
"""A ordem 10 dos tres representantes de tamanho 4, e a peneira na ordem 8."""
from math import factorial

from padroes.medidas import serie
from padroes.varredura import contar, contar_peneirando


def test_a_ordem_10_das_tres_classes():
    assert serie((1, 2, 3, 4), 10) == [1, 2, 6, 23, 103, 513, 2761, 15767,
                                       94359, 586590]
    assert serie((1, 3, 2, 4), 10) == [1, 2, 6, 23, 103, 513, 2762, 15793,
                                       94776, 591950]
    assert serie((1, 3, 4, 2), 10) == [1, 2, 6, 23, 103, 512, 2740, 15485,
                                       91245, 555662]


def test_a_ordem_das_tres_classes_nao_muda():
    # 1342 < 1234 < 1324 em toda ordem a partir da setima.
    a = serie((1, 3, 4, 2), 10)
    b = serie((1, 2, 3, 4), 10)
    c = serie((1, 3, 2, 4), 10)
    for n in range(7, 11):
        assert a[n - 1] < b[n - 1] < c[n - 1], n


def test_a_fracao_que_evita_desaba():
    serie_1234 = serie((1, 2, 3, 4), 10)
    fracao = serie_1234[-1] / factorial(10)
    assert round(100 * fracao, 4) == 16.1648
    assert round(100 * serie_1234[4] / factorial(5), 2) == 85.83


def test_peneirar_a_ordem_8_inteira():
    # 40.320 permutacoes abertas uma a uma, contra o caminho que cresce.
    for p in ((1, 2, 3, 4), (1, 3, 2, 4), (1, 3, 4, 2)):
        assert contar_peneirando(8, p) == contar(8, p), p


def test_as_diferencas_entre_as_classes():
    a = serie((1, 3, 4, 2), 10)
    b = serie((1, 2, 3, 4), 10)
    c = serie((1, 3, 2, 4), 10)
    assert c[6] - b[6] == 1          # ordem 7: uma permutacao de diferenca
    assert c[8] - b[8] == 417        # ordem 9
    assert c[9] - b[9] == 5360       # ordem 10
    assert round(100 * (1 - a[9] / c[9]), 2) == 6.13
