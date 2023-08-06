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

from collections import Counter
from functools import cache

import numpy as np
import pandas as pd

from ..corpus import Corpus
from .hierarchical_block_map import composite_hierarchical_block_map
from . import zmethods
from .tables import subxblocks_report, xblocks_report
from .network_map import network_map


class Blocks:
    """
    Methods to produce visualisations and analysis from an existing blockstate.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.col_title is None:
            print("Warning: `col_title` is not set")

    def get_blocks_levels(self, btype=None):
        """
        Parameters
        ----------
        btype: the type of block to return ('doc', 'ter' or 'ext')

        Returns
        -------
        blocks: the original blocks
        levels: the levels
        """
        if btype is None:
            return {
                "doc": (self.dblocks, self.dblocks_levels),
                "ter": (self.tblocks, self.tblocks_levels),
                "ext": (self.eblocks, self.eblocks_levels),
            }
        elif btype == "doc":
            return self.dblocks, self.dblocks_levels
        elif btype == "ter":
            return self.tblocks, self.tblocks_levels
        elif btype == "ext":
            return self.eblocks, self.eblocks_levels
        else:
            raise ValueError("Unrecognized `btype`.")

    def get_blocks_levels_sample(self, btype):
        """
        If data is sampled, we need to sample the corresponding entries
        from the blocks as well.

        Parameters
        ----------
        btype: the type of block to return ('doc', 'ter' or 'ext')

        Returns
        -------
        blocks: the original blocks
        levels: the levels
        sblocks: the blocks restricted to the data sample
        """
        blocks, levels = self.get_blocks_levels(btype)
        if btype == "doc":
            sblocks = self.dblocks.loc[self.data.index]
        elif btype == "ter":
            sblocks = self.tblocks.loc[
                self.tblocks.index.intersection(self.get_vocab())
            ]
        elif btype == "ext":
            sblocks = blocks  # TODO actually sample eblocks
        return blocks, levels, sblocks

    def hblock_to_level_block(self, hb, btype):
        _, levels = self.get_blocks_levels(btype)
        level = len(levels) - len(hb) + 1
        return ("v" if level == 0 else level), hb[-1]

    def level_block_to_hblock(self, level, block, btype):
        blocks, levels = self.get_blocks_levels(btype)
        if level == "v":
            levels = levels.copy()
            levels.insert(0, "v")
        b = blocks.loc[blocks[level].eq(block), levels[levels.index(level) :]]
        return tuple(reversed(b.iloc[0].tolist()))

    def domain_labels_to_selection(self, labels):
        level_blocks = {}
        for label in labels:
            for level, block in [
                self.hblock_to_level_block(self.label_to_hblock[label], "doc")
            ]:
                level_blocks.setdefault(level, []).append(block)
        sel = pd.Series(False, self.data.index)
        for level, blocks in level_blocks.items():
            sel |= self.dblocks[level].isin(blocks)
        return sel

    def set_sample(self, sample, keep=False):
        Corpus.set_sample(self, sample=sample, keep=keep)
        if hasattr(self, "dblocks"):
            if not hasattr(self, "_orig_dblocks"):
                self._orig_dblocks = self.dblocks
            if keep:
                self.dblocks = self.dblocks.loc[self.data.index]
            else:
                self.dblocks = self._orig_dblocks.loc[self.data.index]

    def find_blocks(self, lscape, finder):
        """
        Returns the blocks that correspond to features defined in finder.
        For example, blocks with the highest or lowest values, or with
        the highest or lowest differences in values across the landscape.

        Parameters
        ----------
        lscape: dict of pandas.Series or pandas.DataFrames
            The landscape of values for each level over its blocks.
        finder: str or function
            Finds the desired blocks in the landscape.

        Returns
        -------
        found: dict
            Dictionary containing whatever `finder` looked for.
        """
        if callable(finder):
            return finder(self, lscape)

        found = dict()
        if finder == "level_max_min_absmin":
            for level, ls_l in lscape.items():
                if isinstance(ls_l, pd.Series):
                    found[level] = dict(
                        max=ls_l.idxmax, min=ls_l.idxmin, absmin=ls_l.abs().idxmin()
                    )
                elif isinstance(ls_l, pd.DataFrame):
                    idxmax = ls_l.max().idxmax()
                    idxmin = ls_l.min().idxmin()
                    idxabsmin = ls_l.abs().min().idxmin()
                    found[level] = dict(
                        max=(ls_l.idxmax()[idxmax], idxmax),
                        min=(ls_l.idxmin()[idxmin], idxmin),
                        absmin=(ls_l.abs().idxmin()[idxabsmin], idxabsmin),
                    )
                else:
                    raise ValueError("Unrecognized type in values of `lscape`.")
        return found

    def domain_map(self, title=None, diff_idxs=None, chained=False, **kwargs):
        idx_all = self.data.index.copy()
        idx_all.name = "all"
        btype = "ext" if chained else "ter"

        if not diff_idxs:
            kwargs_ = dict(
                norm=["bylevelmax", "bylevelmax"],
                scale=["linear", "linear"],
                bheight=["proval", "hierarchical"],
            )
            kwargs_.update(kwargs)
            return composite_hierarchical_block_map(
                self,
                ["doc", btype],
                zmethod=[
                    zmethods.density,
                    zmethods.x_link_density_gen(btype),
                ],
                link_p_func=zmethods.p_rel,
                page_title=title,
                **kwargs_,
            )

        else:
            idx0, idx1 = diff_idxs
            kwargs_ = dict(
                norm=["bylevelmax", "bylevelmax"],
                scale=["linear", "log"],
                bheight=["proval", "hierarchical"],
            )
            kwargs_.update(kwargs)
            return composite_hierarchical_block_map(
                self,
                ["doc", btype],
                zmethod=[
                    zmethods.density_pair_gen(idx0, idx1, zmethods.p_diff),
                    zmethods.x_link_density_pair_gen(idx0, idx1, zmethods.p_rel, btype),
                ],
                link_p_func=zmethods.p_rel,
                page_title=title,
                **kwargs_,
            )

    def subxblocks_tables(self, xbtype, xlevel, xb, ybtype, ylevel=1):
        outpaths = []
        outdir = self.blocks_adir if ybtype == "ter" else self.chained_adir
        if xb is None:
            xblocks, _ = self.get_blocks_levels(xbtype)
            xbtargets = xblocks[xlevel].unique()
        elif isinstance(xb, list):
            xbtargets = xb
        else:
            xbtargets = [xb]
        for xbt in xbtargets:
            if sample_hash := self.get_sample_hash(doc=True, ter=True, ext=True):
                sample_hash = f"-sample:{sample_hash}"
            outfile = f"table{sample_hash}-{self.lblock_to_label[xlevel, xbt]}"
            outfile += f"-L{ylevel}{ybtype[0].upper()}.html"
            fname = subxblocks_report(
                self,
                xbtype,
                xlevel,
                xbt,
                ybtype,
                ylevel,
                outfile=outdir / outfile,
            )
            outpaths.append(fname)
        return outpaths if isinstance(xb, list) or xb is None else outpaths.pop()

    def xblocks_tables(self, *args, **kwargs):
        return xblocks_report(self, *args, **kwargs)

    def domain_network(self, *args, **kwargs):
        return network_map(self, "doc", *args, **kwargs)

    def network_map(self, *args, **kwargs):
        return network_map(self, *args, **kwargs)

    def filter_topic_terms_from_corpus(self, tlevel, tblock, column=None):
        """
        Removes all terms belonging to a topic from the corpus.
        """
        topic_terms = set(self.tblocks[self.tblocks[tlevel].eq(tblock)].index)
        return self.filter_terms(lambda term: term not in topic_terms, column)

    @cache
    def get_xelement_yelements(self, xbtype, ybtype):
        if (xbtype, ybtype) == ("doc", "ter"):
            return self.get_doc_terms()
        if (xbtype, ybtype) == ("doc", "ext"):
            return self.get_doc_exts()
        if (xbtype, ybtype) == ("ter", "doc"):
            return pd.Series(self.ter_documents, index=self.tblocks.index).map(
                lambda x: Counter() if x is np.nan else x
            )
        if (xbtype, ybtype) == ("ext", "doc"):
            return pd.Series(self.ext_documents, index=self.eblocks.index).map(
                lambda x: Counter() if x is np.nan else x
            )

    @cache
    def get_xblock_yblocks_counts(self, xbtype, xlevel, xb, ybtype, ylevel):
        xelement_yelements = self.get_xelement_yelements(xbtype, ybtype)
        xblocks, _ = self.get_blocks_levels(xbtype)
        yblocks, _ = self.get_blocks_levels(ybtype)
        sel = xb if xlevel is None else xblocks[xlevel].eq(xb)
        yelement2yblock = (lambda x: x) if ylevel is None else yblocks[ylevel].get
        xblock_yblocks_c = Counter()
        if hasattr(xelement_yelements.iloc[0], "elements"):  # e.g. Counter()
            for val in xelement_yelements.loc[sel]:
                xblock_yblocks_c.update(yelement2yblock(el) for el in val.elements())
        else:
            for val in xelement_yelements.loc[sel]:
                xblock_yblocks_c.update(yelement2yblock(el) for el in val)
        return xblock_yblocks_c

    def get_xblock_yblocks_stat(
        self, stat, xbtype, xlevel, xb, ybtype, ylevel, ybs=None
    ):
        """
        Gets the `stat` = "count" or "frac_presence" of yblocks in xblocks.
        """
        ybs = None if ybs is None else set(ybs)
        if stat not in ("count", "frac_presence"):
            raise ValueError(f"Unkown statistics: {stat}")
        xelements_yelements = self.get_xelement_yelements(xbtype, ybtype)
        xblocks, _ = self.get_blocks_levels(xbtype)
        yblocks, _ = self.get_blocks_levels(ybtype)

        # functions to abstract different cases
        yelement2yblock = (lambda x: x) if ylevel is None else yblocks[ylevel].get
        yels_is_counter = hasattr(xelements_yelements.iloc[0], "elements")
        yelements2yblocks = (
            (lambda xel_yels: (yelement2yblock(el) for el in xel_yels.elements()))
            if yels_is_counter
            else (lambda xel_yels: (yelement2yblock(el) for el in xel_yels))
        )
        yelements2yblocks4stat = (
            yelements2yblocks
            if (stat == "count")
            else (lambda xel_yels: set(yelements2yblocks(xel_yels)))
        )
        any_func = len if stat == "count" else bool

        # calculations
        xblock_yblocks_c = Counter()
        xblock_yblocks_any = 0
        sel = (xblocks.index == xb) if xlevel is None else xblocks[xlevel].eq(xb)
        for xel_yels in xelements_yelements.loc[sel]:
            yblocks4stat = [*yelements2yblocks4stat(xel_yels)]
            xblock_yblocks_c.update(yblocks4stat)
            xblock_yblocks_any += any_func(
                [yb for yb in yblocks4stat if (ybs is None) or (yb in ybs)]
            )

        stat_s = pd.Series(xblock_yblocks_c).sort_values()
        stat_s.name = self.lblock_to_label[xlevel, xb]
        stat_s["any"] = xblock_yblocks_any
        stat_s = stat_s.div(sel.sum()) if stat == "frac_presence" else stat_s
        return stat_s

    def get_dblock_xcount(self, b, btype):
        dlevel, db = self.hblock_to_level_block(b, "doc")
        xc = self.get_xblock_yblocks_counts("doc", dlevel, db, btype, None)
        xct = sum(xc.values())
        return xc, xct

    def get_dblock_xblock_count(self, b, btype):
        dlevel, db = self.hblock_to_level_block(b, "doc")
        xc = self.get_xblock_yblocks_counts("doc", dlevel, db, btype, 1)
        xct = sum(xc.values())
        return xc, xct
