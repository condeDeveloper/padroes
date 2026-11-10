# -*- coding: utf-8 -*-
"""Conter um padrao, pelos dois caminhos, e o grupo das oito simetrias."""
from itertools import permutations
from math import factorial

from padroes.nucleo import (complemento, contem, contem_na_marra, evita,
                            inverso, orbitas, padrao_de, reverso, simetrias,
                            todos_os_padroes)


def test_forma_de_uma_sequencia():
    assert padrao_de((30, 10, 40)) == (2, 1, 3)
    assert padrao_de((5,)) == (1,)
    assert padrao_de((4, 3, 2, 1)) == (4, 3, 2, 1)
    assert padrao_de(()) == ()


def test_casos_escritos_a_mao():
    assert contem((3, 1, 4, 2), (2, 1, 3))
    assert not contem((3, 1, 4, 2), (2, 4, 1, 3))
    assert contem((2, 4, 1, 3), (2, 4, 1, 3))
    assert not contem((1, 2, 3), (3, 2, 1))
    assert contem((1, 2, 3), (1, 2, 3))
    assert evita((2, 1), (1, 2))


def test_padrao_maior_que_a_permutacao_nunca_cabe():
    for n in range(1, 4):
        for p in permutations(range(1, n + 1)):
            assert not contem(p, (1, 2, 3, 4, 5))
            assert evita(p, (1, 2, 3, 4, 5))


def test_os_dois_testes_concordam_em_toda_permutacao_pequena():
    for n in range(1, 7):
        for p in permutations(range(1, n + 1)):
            for padrao in todos_os_padroes(3):
                assert contem(p, padrao) == contem_na_marra(p, padrao), (p, padrao)


def test_os_dois_testes_concordam_com_padrao_de_tamanho_4():
    for n in range(1, 7):
        for p in permutations(range(1, n + 1)):
            for padrao in ((1, 3, 2, 4), (2, 4, 1, 3), (1, 2, 3, 4)):
                assert contem(p, padrao) == contem_na_marra(p, padrao), (p, padrao)


def test_inverso_reverso_e_complemento():
    assert inverso((2, 3, 1)) == (3, 1, 2)
    assert inverso(inverso((2, 3, 1))) == (2, 3, 1)
    assert reverso((2, 3, 1)) == (1, 3, 2)
    assert complemento((2, 3, 1)) == (2, 1, 3)
    for p in todos_os_padroes(4):
        assert reverso(reverso(p)) == p
        assert complemento(complemento(p)) == p
        assert inverso(inverso(p)) == p


def test_as_simetrias_sao_no_maximo_oito():
    for k in (2, 3, 4):
        for p in todos_os_padroes(k):
            grupo = simetrias(p)
            assert 1 <= len(grupo) <= 8
            assert tuple(p) in grupo


def test_as_orbitas_cobrem_tudo_sem_repetir():
    for k in (2, 3, 4, 5):
        grupos = orbitas(k)
        vistos = set()
        for g in grupos:
            for p in g:
                assert p not in vistos
                vistos.add(p)
        assert len(vistos) == factorial(k)


def test_os_tamanhos_das_orbitas():
    assert [len(g) for g in orbitas(3)] == [2, 4]
    assert [len(g) for g in orbitas(4)] == [2, 4, 2, 8, 4, 2, 2]
    assert sum(len(g) for g in orbitas(4)) == 24


def test_simetria_leva_evitante_em_evitante():
    # Se p vira q por uma simetria, as evitantes de p viram as de q pela MESMA
    # simetria. Aqui so a consequencia que da para medir barato.
    for p in todos_os_padroes(3):
        for q in (reverso(p), complemento(p), inverso(p)):
            contagem_p = sum(1 for x in permutations(range(1, 6)) if evita(x, p))
            contagem_q = sum(1 for x in permutations(range(1, 6)) if evita(x, q))
            assert contagem_p == contagem_q
