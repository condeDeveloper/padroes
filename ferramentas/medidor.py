# -*- coding: utf-8 -*-
"""Imprime as tabelas que vao para o README. Nenhum numero sai daqui a mao.

    python ferramentas/medidor.py          ate a ordem 9
    python ferramentas/medidor.py --tudo   inclui a ordem 10 dos tres
                                           representantes de tamanho 4
"""
from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from padroes.juiz import catalanos  # noqa: E402
from padroes.medidas import (resumo_das_orbitas, serie,  # noqa: E402
                             tabela_orbitas, tabela_separacao,
                             tabela_tamanho_3, tabela_wilf)
from padroes.varredura import desacordos_entre_os_dois_testes  # noqa: E402


def nome(p) -> str:
    return "".join(str(v) for v in p)


def titulo(texto: str) -> None:
    print()
    print(texto)
    print("-" * len(texto))


def tamanho3() -> None:
    titulo("Os seis padroes de tamanho 3")
    print("  padrao  contagens ate a ordem 9")
    for p, c, bate in tabela_tamanho_3():
        print("  %-7s %s%s" % (nome(p), c, "" if bate else "   NAO E CATALAN"))
    print("  Catalan %s" % catalanos(9))
    quantas, tamanhos, cobrem = resumo_das_orbitas(3)
    print("  as simetrias so juntam %d orbitas, de tamanhos %s (cobrem tudo: %s)"
          % (quantas, tamanhos, cobrem))


def orbitas4() -> None:
    titulo("Os padroes de tamanho 4, por orbita de simetria")
    quantas, tamanhos, cobrem = resumo_das_orbitas(4)
    print("  %d orbitas, de tamanhos %s (cobrem tudo: %s)"
          % (quantas, tamanhos, cobrem))
    print("  representante  padroes  contagens ate a ordem 9")
    for rep, tamanho, c in tabela_orbitas(4):
        print("  %-14s %-8d %s" % (nome(rep), tamanho, c))


def wilf() -> None:
    titulo("As classes de CONTAGEM: sete orbitas, tres respostas")
    for c, padroes, orbitas_na_classe, representantes in tabela_wilf():
        print("  %2d padroes em %d orbitas: %s"
              % (padroes, orbitas_na_classe,
                 " ".join(nome(r) for r in representantes)))
        print("     %s" % c)
    titulo("Onde cada par de classes comeca a divergir")
    for a, b, ordem in tabela_separacao():
        print("  %s contra %s: a partir da ordem %d" % (nome(a), nome(b), ordem))


def dois_testes() -> None:
    titulo("Os dois testes de 'contem', permutacao por permutacao")
    for n in range(1, 8):
        inicio = time.time()
        ruins = desacordos_entre_os_dois_testes(n, (2, 4, 1, 3))
        print("  n=%-3d %d desacordos  (%.1fs)" % (n, ruins, time.time() - inicio))


def ordem10() -> None:
    titulo("A ordem 10 dos tres representantes")
    for rep in ((1, 2, 3, 4), (1, 3, 2, 4), (1, 3, 4, 2)):
        inicio = time.time()
        c = serie(rep, 10)
        print("  %-6s %s  (%.1fs)" % (nome(rep), c, time.time() - inicio))


def main() -> int:
    tudo = "--tudo" in sys.argv
    tamanho3()
    orbitas4()
    wilf()
    dois_testes()
    if tudo:
        ordem10()
    else:
        print()
        print("(a ordem 10 so com --tudo)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
