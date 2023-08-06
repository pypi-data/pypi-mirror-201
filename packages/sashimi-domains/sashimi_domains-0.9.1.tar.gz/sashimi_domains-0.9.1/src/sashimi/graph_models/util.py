# coding: utf-8

# Sashimi - Study of the organisation and evolution of a corpus
#
# Author(s):
# * Ale Abdo <abdo@member.fsf.org>
#
# License:
# [GNU-GPLv3+](https://www.gnu.org/licenses/gpl-3.0.html)
#
# Project:
# <https://en.wikiversity.org/wiki/The_dynamics_and_social_organization_of
#  _innovation_in_the_field_of_oncology>
#
# Reference repository for this file:
# <https://gitlab.com/solstag/abstractology>
#
# Contributions are welcome, get in touch with the author(s).


def contiguous_map_nested_blockstate(ns, io_is_bs=False):
    bs = ns if io_is_bs else ns.get_bs()
    bs = [b.copy() for b in bs]
    for lvl, b in enumerate(bs):
        m = dict()
        for i, b_i in enumerate(b):
            b[i] = m.setdefault(b_i, len(m))
        if lvl + 1 < len(bs):
            up_b = bs[lvl + 1]
            up_bc = up_b[: len(m)].copy()
            for i, j in m.items():
                up_bc[j] = up_b[i]
            bs[lvl + 1] = up_bc
    while len(bs) > 2 and list(bs[-1]) == list(bs[-2]):
        bs.pop()
    return bs if io_is_bs else ns.copy(bs=bs)
