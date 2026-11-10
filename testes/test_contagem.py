# -*- coding: utf-8 -*-
"""A contagem contra Catalan, contra a peneira e contra as simetrias."""
from math import factorial

from padroes.juiz import (as_orbitas_cobrem_tudo, catalanos,
                          classes_de_wilf, limites_plausiveis,
                          primeira_ordem_que_separa)
from padroes.nucleo import orbitas, todos_os_padroes
from padroes.varredura import (contagens, contar, contar_peneirando,
                               desacordos_entre_os_dois_testes)


def test_os_seis_padroes_de_tamanho_3_dao_catalan():
    alvo = catalanos(9)
    for p in todos_os_padroes(3):
        assert contagens(9, p) == alvo, p
    assert alvo == [1, 2, 5, 14, 42, 132, 429, 1430, 4862]


def test_crescer_e_peneirar_dao_o_mesmo():
    for p in ((1, 3, 2), (3, 2, 1), (1, 3, 2, 4), (2, 4, 1, 3)):
        for n in range(1, 8):
            assert contar(n, p) == contar_peneirando(n, p), (p, n)


def test_os_dois_testes_de_contem_nao_discordam():
    for n in range(1, 7):
        assert desacordos_entre_os_dois_testes(n, (2, 4, 1, 3)) == 0, n
        assert desacordos_entre_os_dois_testes(n, (1, 2, 3)) == 0, n


def test_as_tres_series_de_tamanho_4():
    assert contagens(9, (1, 2, 3, 4)) == [1, 2, 6, 23, 103, 513, 2761, 15767, 94359]
    assert contagens(9, (1, 3, 2, 4)) == [1, 2, 6, 23, 103, 513, 2762, 15793, 94776]
    assert contagens(9, (1, 3, 4, 2)) == [1, 2, 6, 23, 103, 512, 2740, 15485, 91245]


def test_padroes_da_mesma_orbita_contam_igual():
    for grupo in orbitas(4):
        alvo = contagens(8, grupo[0])
        for p in grupo:
            assert contagens(8, p) == alvo, p


def test_as_orbitas_cobrem_tudo():
    for k in (2, 3, 4, 5):
        assert as_orbitas_cobrem_tudo(k), k


def test_sete_orbitas_mas_tres_classes():
    por_padrao = {}
    for grupo in orbitas(4):
        c = contagens(9, grupo[0])
        for p in grupo:
            por_padrao[p] = c
    classes = classes_de_wilf(por_padrao)
    assert len(orbitas(4)) == 7
    assert len(classes) == 3
    assert sorted(len(c) for c in classes) == [2, 10, 12]


def test_quando_cada_classe_comeca_a_divergir():
    a = contagens(9, (1, 2, 3, 4))
    b = contagens(9, (1, 3, 4, 2))
    c = contagens(9, (1, 3, 2, 4))
    assert primeira_ordem_que_separa(a, b) == 6
    assert primeira_ordem_que_separa(a, c) == 7
    assert primeira_ordem_que_separa(b, c) == 6
    # Ate a ordem 5 os vinte e quatro padroes sao indistinguiveis.
    assert a[:5] == b[:5] == c[:5] == [1, 2, 6, 23, 103]


def test_os_limites_valem_em_todo_padrao_de_tamanho_4():
    for grupo in orbitas(4):
        assert limites_plausiveis(4, contagens(8, grupo[0])), grupo[0]


def test_a_contagem_e_n_fatorial_ate_o_tamanho_do_padrao():
    for k in (3, 4):
        for p in (todos_os_padroes(k)[0], todos_os_padroes(k)[-1]):
            c = contagens(6, p)
            for n in range(1, k):
                assert c[n - 1] == factorial(n), (p, n)
            assert c[k - 1] == factorial(k) - 1
