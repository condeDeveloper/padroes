# -*- coding: utf-8 -*-
"""Linha de comando: `python -m padroes <comando>`.

    contar <padrao> [ate]   quantas permutacoes evitam o padrao, por ordem
    orbitas <k>             os padroes de tamanho k agrupados pelas simetrias
    wilf [ate]              as classes de contagem dos padroes de tamanho 4
    testar <perm> <padrao>  essa permutacao contem esse padrao?
"""
from __future__ import annotations

import sys

from .medidas import serie, tabela_wilf
from .nucleo import contem, contem_na_marra, orbitas


def _padrao(texto) -> tuple:
    return tuple(int(c) for c in texto)


def _contar(args) -> int:
    if not args:
        print("falta o padrao, por exemplo 1324", file=sys.stderr)
        return 2
    p = _padrao(args[0])
    ate = int(args[1]) if len(args) > 1 else 9
    for n, quantas in enumerate(serie(p, ate), start=1):
        print("  n=%-3d %d" % (n, quantas))
    return 0


def _orbitas(args) -> int:
    k = int(args[0]) if args else 4
    for grupo in orbitas(k):
        print("  %s" % " ".join("".join(str(v) for v in p) for p in grupo))
    return 0


def _wilf(args) -> int:
    ate = int(args[0]) if args else 9
    for c, padroes, quantas, representantes in tabela_wilf(4, ate):
        print("  %d padroes em %d orbitas: %s"
              % (padroes, quantas,
                 " ".join("".join(str(v) for v in r) for r in representantes)))
        print("    %s" % c)
    return 0


def _testar(args) -> int:
    if len(args) < 2:
        print("uso: testar <permutacao> <padrao>", file=sys.stderr)
        return 2
    perm, padrao = _padrao(args[0]), _padrao(args[1])
    print("com poda:  %s" % contem(perm, padrao))
    print("na marra:  %s" % contem_na_marra(perm, padrao))
    return 0


COMANDOS = {"contar": _contar, "orbitas": _orbitas, "wilf": _wilf,
            "testar": _testar}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] not in COMANDOS:
        print(__doc__)
        return 0 if not argv else 2
    return COMANDOS[argv[0]](argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
