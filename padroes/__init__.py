# -*- coding: utf-8 -*-
"""Permutacoes que evitam um padrao, contadas crescendo.

O pacote tem quatro pedacos que nao se misturam:

    nucleo     o que e conter um padrao, por dois caminhos, e as simetrias
    varredura  conta as evitantes de cada ordem, crescendo da anterior
    juiz       Catalan, simetria e as bordas, cobrados da contagem
    medidas    as tabelas que vao para o README
"""
from .juiz import (as_orbitas_cobrem_tudo, catalan, catalanos,
                   classes_de_wilf, limites_plausiveis, mesma_orbita,
                   primeira_ordem_que_separa, quantas_orbitas,
                   tamanho_das_orbitas)
from .nucleo import (complemento, contem, contem_na_marra, evita, inverso,
                     orbitas, padrao_de, reverso, simetrias, todos_os_padroes)
from .varredura import (Rodada, contagens, contar, contar_peneirando, crescer,
                        desacordos_entre_os_dois_testes)

__all__ = [
    "Rodada", "as_orbitas_cobrem_tudo", "catalan", "catalanos",
    "classes_de_wilf", "complemento", "contagens", "contar",
    "contar_peneirando", "contem", "contem_na_marra", "crescer",
    "desacordos_entre_os_dois_testes", "evita", "inverso",
    "limites_plausiveis", "mesma_orbita", "orbitas", "padrao_de",
    "primeira_ordem_que_separa", "quantas_orbitas", "reverso", "simetrias",
    "tamanho_das_orbitas", "todos_os_padroes",
]

__version__ = "1.0.0"
