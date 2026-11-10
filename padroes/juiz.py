# -*- coding: utf-8 -*-
"""O juiz: o que a contagem e obrigada a cumprir, sem olhar a varredura.

1. **Knuth, 1968.** Os seis padroes de tamanho 3 sao evitados por exatamente
   `C(2n, n) / (n+1)` permutacoes de tamanho n -- os numeros de Catalan. Que os
   SEIS deem o mesmo numero nao e simetria: as simetrias so juntam `123` com
   `321` e os outros quatro entre si, duas orbitas. Que as duas orbitas
   coincidam e o teorema.
2. **Simetria.** Inverter, ler de tras para frente e virar de cabeca para baixo
   levam subsequencia em subsequencia. Entao padroes na mesma orbita sao
   contados IGUAL em toda ordem, e isso vale sem teorema nenhum.
3. **Bordas.** Toda permutacao de tamanho menor que o padrao o evita: a
   contagem comeca valendo n! e so desce quando n alcanca o tamanho do padrao.
4. **Monotonia.** A contagem nunca desce quando n cresce, e nunca passa de n!.

O juiz nao sabe contar evitantes. Ele sabe o que o resultado tem de obedecer.
"""
from __future__ import annotations

from math import comb, factorial

from .nucleo import orbitas, simetrias


def catalan(n: int) -> int:
    return comb(2 * n, n) // (n + 1)


def catalanos(ate: int) -> list[int]:
    return [catalan(n) for n in range(1, ate + 1)]


def mesma_orbita(p, q) -> bool:
    return tuple(q) in simetrias(p)


def quantas_orbitas(k: int) -> int:
    return len(orbitas(k))


def tamanho_das_orbitas(k: int) -> list[int]:
    return [len(g) for g in orbitas(k)]


def as_orbitas_cobrem_tudo(k: int) -> bool:
    """A soma dos tamanhos das orbitas e k!, e nenhum padrao aparece duas vezes."""
    grupos = orbitas(k)
    vistos: set = set()
    for g in grupos:
        for p in g:
            if p in vistos:
                return False
            vistos.add(p)
    return len(vistos) == factorial(k)


def limites_plausiveis(k: int, contagens) -> bool:
    """A contagem comeca em n!, nunca desce e nunca passa de n!."""
    anterior = -1
    for i, valor in enumerate(contagens):
        n = i + 1
        if valor > factorial(n):
            return False
        if valor < anterior:
            return False
        if n < k and valor != factorial(n):
            return False
        anterior = valor
    return True


def classes_de_wilf(contagens_por_padrao) -> list[list]:
    """Agrupa padroes pela SEQUENCIA de contagens, nao pela simetria.

    Recebe `{padrao: contagens}` e devolve os grupos, em ordem. Duas orbitas de
    simetria que caem no mesmo grupo sao uma coincidencia de contagem que a
    simetria nao explica -- e e exatamente ai que mora o assunto.
    """
    grupos: dict = {}
    for padrao, contagens in contagens_por_padrao.items():
        grupos.setdefault(tuple(contagens), []).append(padrao)
    return [sorted(v) for _k, v in sorted(grupos.items())]


def primeira_ordem_que_separa(a, b) -> int:
    """A menor ordem em que duas sequencias de contagem divergem, ou -1."""
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i + 1
    return -1
