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


import graph_tool.all as gt
import numpy
import pandas
from pathlib import Path
import shutil

from ..misc import clearattrs, makep_fromdict, property_getfuncdir
from ..ioio import ioio
from ..corpus import Corpus
from ..scorology import Scorology
from ..blocks import Blocks, zmethods
from ..blocks.util import sorted_hierarchical_block_index

from .domain_topic_model import create_docter_graph, calc_nested_blockstate
from .domain_chained_model import (
    extend_graph,
    gen_doc_graph,
    calc_chained_nested_blockstate,
)


class GraphModels(Blocks, Scorology, Corpus):
    """
    Build graphs from corpora and find optimal block models.
    """

    def __init__(self, *args, **kwargs):
        """
        Call `super()` to set up the stage then add class specifics.
        """
        super().__init__(*args, **kwargs)

        self.set_graph(self._to_load.pop("graph", None), strict=False)
        self.set_blockstate(self._to_load.pop("blockstate", None))
        self.loaded["chainedbstates"] = self._to_load.pop("chainedbstates", {})
        if graph_extend := self._to_load.pop("graph_extend", None):
            self.set_chain(**graph_extend, strict=False)
        else:
            self.unset_chain()

    ext_g = ".gt.xz"
    ext_nbs = ".json.xz"

    graph_name = makep_fromdict("loaded", "graph", True, None, None)
    graph_dir = property_getfuncdir(lambda self: self.data_dir / self.graph_name)
    graph_adir = property_getfuncdir(lambda self: self.data_adir / self.graph_name)
    blocks_name = makep_fromdict("loaded", "blockstate", True, None, None)
    blocks_dir = property_getfuncdir(lambda self: self.graph_dir / self.blocks_name)
    blocks_adir = property_getfuncdir(lambda self: self.graph_adir / self.blocks_name)
    graph_extend = makep_fromdict("loaded", "graph_extend", True, None, None)
    graph_extend_name = property(lambda self: str(tuple(self.graph_extend.values())))
    chained_name = property(
        lambda self: self.loaded["chainedbstates"].get(self.graph_extend_name, None)
    )
    chained_dir = property_getfuncdir(lambda self: self.blocks_dir / self.chained_name)
    chained_adir = property_getfuncdir(
        lambda self: self.blocks_adir / self.chained_name
    )

    def load_domain_topic_model(self, ltype="link", load=True):
        """"""
        self.cache_clear(clear_static=True)
        if not self.column:
            raise ValueError
        if not self.blocks_name or not load:
            if not self.graph_name:
                create_docter_graph(self)
            self.load_graph()
            calc_nested_blockstate(self)
        self.load_blockstate()
        self.blockstate_to_dataframes()
        self.load_ter_documents()
        zmethods.load_cross_count_all(self, "ter", "link")

    def load_domain_chained_model(
        self, ltype="link", load=True, bext="max", anneal=False
    ):
        """"""
        self.cache_clear(clear_static=True)
        if not (self.graph_extend and (load or self.blocks_name)):
            raise ValueError
        self.load_blockstate()
        self.blockstate_to_dataframes()
        if not self.chained_name or not load:
            calc_chained_nested_blockstate(self, bext=bext, anneal=anneal)
        self.load_blockstate(chained=True, keep_blocks=True)
        self.blockstate_to_dataframes()
        self.load_ter_documents()
        self.load_ext_documents()
        zmethods.load_cross_count_all(self, "ter", "link")
        zmethods.load_cross_count_all(self, "ext", "link")

    def trim_to_sample(self):
        self.cache_clear(clear_static=True)
        self.cached_annotations = False
        self.cached_cross_count = False
        if not self.tblocks.empty:
            self.load_ter_documents()
            if not hasattr(self, "_orig_tblocks"):
                self._orig_tblocks = self.tblocks.copy()
            self.tblocks = self._orig_tblocks[
                self._orig_tblocks.index.isin(self.ter_documents)
            ]
            zmethods.load_cross_count_all(self, "ter", "link")
        if not self.eblocks.empty:
            self.load_ext_documents()
            if not hasattr(self, "_orig_eblocks"):
                self._orig_eblocks = self.eblocks.copy()
            self.eblocks = self._orig_eblocks[
                self._orig_eblocks.index.isin(self.ext_documents)
            ]
            zmethods.load_cross_count_all(self, "ext", "link")

    ################################################
    # Graph and blockstate methods (TODO move out) #
    ################################################

    def from_corpus_to_convoc(self):
        """
        Builds a bipartite undirected graph of terms connecting to the contexts
        they appear in.

        TODO: perhaps a directed graph where contexts connect back their
        composing terms?

        Parameters
        ----------
        """
        pass

    def annotate_graph(self, g, vprops=[], eprops=[]):
        """
        Add properties to the vertices and edges of the graph

        Parameters
        ----------
        g: `graph_tool:Graph`
        vprops: `list`
          Columns from `self.data`
        eprops: `list`
          Columns from `self.data`

        Returns
        -------
        g: the graph, with added properties
        """
        document_ids = self.get_document_ids()
        for prop in eprops:
            g.vp[prop] = g.new_vertex_property(self.get_col_type(prop))
        for prop in eprops:
            g.ep[prop] = g.new_edge_property(self.get_col_type(prop))
        for v in g.vertices():
            sel = document_ids == g.vp["name"][v]
            (di,) = document_ids[sel]
            for prop in vprops:
                g.vp[prop][v] = self.data.loc[di, prop]
            for e in v.out_edges():
                for prop in eprops:
                    g.ep[prop][e] = self.data.loc[di, prop]
        return g

    def search_slice(self, slicerange, g=None, overlap=False, layers=True):
        slice_col = self.col_time
        if g is None:
            g = gt.load_graph(str(self.graph_dir / self.graph_name))

        g.ep["sliced"] = g.new_edge_property("int")
        for sval in slicerange:
            name_args = [("slice-" + slice_col, sval)]
            print("Slicing at {}".format(sval))
            for e in g.edges():
                g.ep["sliced"][e] = g.ep[slice_col][e] > sval
            calc_nested_blockstate(
                self,
                name_args=name_args,
                overlap=overlap,
                g=g,
                state_args=dict(ec=g.ep["sliced"], layers=layers),
            )

    ######################
    # I/O and conversion #
    ######################

    # Graph

    def list_graphs(self):
        return [
            str(fpath.name)
            for fpath in self.data_dir.iterdir()
            if ioio.uncompressed_suffix(fpath)
            == ioio.uncompressed_suffix(Path(f"_{self.ext_g}"))
        ]

    def set_graph(self, name=None, strict=True):
        """
        Set graph to be loaded to `name`. Doesn't load the graph.

        name) `str` or `None` (default)
            Graph to set. If none, keep current graph.
        strict) bool
            Check values are valid.
        """
        if strict:
            if name is not None:
                if not (self.data_dir / name / name).is_file():
                    raise ValueError
        self.loaded["graph"] = name

    def load_graph(self, extend=False):
        """
        Loads a graph previously set by `set_graph` into `self.graph`.
        """
        self.clear_graph()
        graph_path = self.graph_dir / self.graph_name
        self.graph = gt.load_graph(str(graph_path))
        if extend:
            self.clear_extended()
            extend_graph(self)
            print(f"Loaded: {self.graph_name} ({self.graph_extend})\n{self.graph}")
        else:
            print(f"Loaded: {self.graph_name}\n{self.graph}")

    def clear_graph(self):
        clearattrs(self, ["graph"])

    def clear_extended(self):
        clearattrs(
            self,
            ["ext_documents", "values_ext_link_count_all", "values_ext_doc_count_all"],
        )

    def unset_chain(self):
        self.loaded["graph_extend"] = None

    def set_chain(self, prop, matcher=None, strict=True):
        """
        (prop) column where to match patterns from matcher
        (matcher) path, absolute or relative to `self.resources_dir`
        """
        if strict:
            if prop not in self.data:
                raise ValueError
            if matcher is not None:
                if not (self.resources_dir / matcher).is_file():
                    raise ValueError
        self.loaded["graph_extend"] = {"prop": prop, "matcher": matcher}

    # Blockstate

    def list_blockstates(self):
        return [
            str(fpath.name)
            for fpath in self.graph_dir.iterdir()
            if fpath.name.startswith("blockstate; ") and fpath.is_dir()
        ]

    def list_chainedbstates(self):
        return [
            str(fpath.name)
            for fpath in self.blocks_dir.iterdir()
            if fpath.name.startswith("chainedbstate; ") and fpath.is_dir()
        ]

    def load_blockstate(self, chained=False, keep_blocks=False):
        """
        Loads a previously stored blockstate from a json or pickle file.

        The loaded state is found at `self.state`.

        Parameters
        ==========
        chained: loads from `self.blocks_name` if False else `self.chained_name`.
        """
        self.clear_blockstate(keep_blocks=keep_blocks)
        if chained:
            fpath = self.chained_dir / self.chained_name
        else:
            fpath = self.blocks_dir / self.blocks_name
        if ioio.uncompressed_suffix(fpath) == ".pickle":
            assert chained is False
            self.state = ioio.load(fpath, fmt="pickle")
        else:
            obj = ioio.load(fpath, fmt="json")
            args = obj["args"]
            args["bs"] = list(map(numpy.array, args["bs"]))
            if chained:
                graph = gen_doc_graph(self)
                extend_graph(self, graph, obj["graph"]["extended"])
                args["bs"][0] = args["bs"][0][-graph.num_vertices() :]
            else:
                graph = gt.load_graph(str(self.graph_dir / obj["graph"]["name"]))
            for key, val in obj["vp_args"].items():
                if val is not None:
                    args[key] = graph.vp[val]
            for key, val in obj["ep_args"].items():
                if val is not None:
                    args[key] = graph.ep[val]
            if args.get("ec", None) is not None:
                args["base_type"] = gt.LayeredBlockState
            else:
                args.pop("layers", None)
            state_class = getattr(gt.graph_tool.inference, obj["class"])
            self.state = state_class(graph, **args)
            self.extended = obj["graph"]["extended"]
        print(
            f"Loaded: {self.chained_name if chained else self.blocks_name}\n{self.state}"
        )

    def store_blockstate(self, fpath, state=None, pclabel=None, layers=None, ec=None):
        if state is None:
            state = self.state
        obj = {
            "class": type(state).__name__,
            "graph": {
                "name": self.graph_name,
                "extended": getattr(state.g, "_sashimi_extended", {}),
            },
            "args": {
                "bs": list(map(lambda x: list(map(int, x)), state.get_bs())),
                "layers": layers,
            },
            "vp_args": {
                "pclabel": pclabel,
            },
            "ep_args": {"ec": ec},
            "entropy": state.entropy(),
        }
        ioio.store(obj, fpath, fmt="json")
        print(f"Stored: {fpath}")

    def clear_blockstate(self, keep_blocks=False):
        if not keep_blocks:
            clearattrs(
                self,
                [
                    "dblocks",
                    "tblocks",
                    "eblocks",
                    "_orig_dblocks",
                    "_orig_tblocks",
                    "_orig_eblocks",
                    "dblocks_levels",
                    "tblocks_levels",
                    "eblocks_levels",
                ],
            )
        clearattrs(self, ["state"])

    def delete_blockstate(self, blocks_name):
        if blocks_name.startswith("blockstate; "):
            blocks_dir = self.graph_dir / blocks_name
            blocks_adir = self.graph_adir / blocks_name
        if blocks_name.startswith("chainedbstate; "):
            blocks_dir = self.blocks_dir / blocks_name
            blocks_adir = self.blocks_adir / blocks_name
        if blocks_adir.exists():
            shutil.rmtree(blocks_adir)
        shutil.rmtree(blocks_dir)  # delete data last

    def get_blockstate(self, chained=False):
        if chained:
            return self.loaded["chainedbstates"][self.graph_extend_name]
        else:
            return self.loaded["blockstate"]

    def set_blockstate(self, blockstate_name, chained=False):
        """
        (chained) if True, set chained blockstate for current graph extension
        """
        if chained:
            self.loaded["chainedbstates"][self.graph_extend_name] = blockstate_name
        else:
            self.loaded["blockstate"] = blockstate_name

    def set_best_state(
        self, state_list=None, chained=False, delete_non_best=False, index=0
    ):
        """
        Sets the corpus to load the available state with the lowest entropy.

        (chained) searches chained states for current choice of extend
        (delete_non_best) remove all data related to the higher entropy states
        (index) get state with sorted index `index`

        :dict: contains the names and entropies of the available states
        """
        if state_list is None:
            state_list = (
                self.list_chainedbstates() if chained else self.list_blockstates()
            )
        state_ent = {}
        for state in state_list:
            self.set_blockstate(state, chained)
            self.load_blockstate(chained=chained)
            state_ent[state] = self.state.entropy()
        chosen_state = sorted(state_ent.items(), key=lambda x: x[1])[index][0]
        self.set_blockstate(chosen_state, chained)
        self.clear_blockstate()
        if delete_non_best:
            for state in [state for state in state_list if state != chosen_state]:
                self.delete_blockstate(state)
        return state_ent

    # Conversion

    def blockstate_to_dataframes(self, nbstate=None):
        """
        state: the blockstate instance to be turned into dataframes indexed at
        documents and terms
        """
        if nbstate is None:
            nbstate = self.state
        g = nbstate.g

        df = pandas.DataFrame(index=[g.vp["name"][v] for v in g.vertices()])
        df["v"] = [int(v) for v in g.vertices()]
        df["type"] = [g.vp["type"][v] for v in g.vertices()]
        for blevel in range(len(nbstate.levels) - 1):  # treat top blevel later
            blocks = nbstate.project_level(blevel).get_blocks()
            df[blevel + 1] = [blocks[v] for v in g.vertices()]
        # include top blevel if it's vertices don't correspond to "type"
        if len(df[blevel + 1].unique()) > 2:
            blevel += 1
            blocks = nbstate.project_level(blevel).get_blocks()
            df[blevel + 1] = [blocks[v] for v in g.vertices()]

        # make sure highest level matches type then replace it
        level = blevel + 1
        if not df.groupby("type")[level].agg(set).map(len).eq(1).all():
            raise ValueError("multiple top level blocks for type!")
        if not df.groupby(level)["type"].agg(set).map(len).eq(1).all():
            raise ValueError("multiple types for top level block!")
        df[level] = df["type"]

        dblocks = df[df["type"].eq(0)]
        tblocks = df[df["type"].eq(1)]
        eblocks = df[df["type"].gt(1)].copy()

        if tblocks.empty and not eblocks.empty:
            # chained state: only load eblocks, with index starting after other blocks
            self_dblocks = getattr(self, "_orig_dblocks", self.dblocks)
            for dblocks_l, tblocks_l, eblocks_l in zip(
                self_dblocks, self.tblocks, eblocks
            ):
                assert dblocks_l == tblocks_l == eblocks_l
                eblocks_start_num = (
                    max(
                        self_dblocks[dblocks_l].max(),
                        self.tblocks[tblocks_l].max(),
                    )
                    - eblocks[eblocks_l].min()
                    + 1
                )
                eblocks[eblocks_l] = eblocks[eblocks_l].map(
                    lambda x: x + eblocks_start_num
                )
            self.eblocks = eblocks
            self.eblocks_levels = [x for x in self.eblocks if isinstance(x, int)]
        else:
            # align dblocks with data
            document_ids = self.get_document_ids()
            self.dblocks = dblocks.reindex(document_ids)
            self.dblocks.index = self.data.index
            self.dblocks.dropna(inplace=True)
            # if sampled, also keep _orig_dblocks aligned with original data
            if len(self.dblocks) < len(dblocks):
                odata_document_ids = self.get_document_ids(self.odata)
                if not document_ids.equals(odata_document_ids):
                    self._orig_dblocks = dblocks.reindex(odata_document_ids)
                    self._orig_dblocks.index = self.odata.index
                    self._orig_dblocks.dropna(inplace=True)
            # assign remaining blocks and block_levels
            self.tblocks, self.eblocks = (tblocks, eblocks)
            self.dblocks_levels, self.tblocks_levels, self.eblocks_levels = (
                [x for x in blocks if isinstance(x, int)]
                for blocks in (dblocks, tblocks, eblocks)
            )
        self.gen_block_label_correspondence()

    def gen_block_label_correspondence(self):
        self.hblock_to_label = {}
        self.label_to_hblock = {}
        self.label_to_mapindex = {}
        self.label_to_tlblock = {}
        self.lblock_to_label = {}
        self.lblock_to_mapindex = {}
        self_dblocks = getattr(self, "_orig_dblocks", self.dblocks)
        for blocks, levels, btype in [
            (self_dblocks, self.dblocks_levels, "doc"),
            (self.tblocks, self.tblocks_levels, "ter"),
            (self.eblocks, self.eblocks_levels, "ext"),
        ]:
            mapindex = 0
            for level in reversed(levels):
                for i, hblock in enumerate(
                    sorted_hierarchical_block_index(blocks, levels, level)
                ):
                    lblock = (level, hblock[-1])
                    label = "L{}{}{}".format(level, btype[0].upper(), i)
                    self.hblock_to_label[hblock] = label
                    self.label_to_hblock[label] = hblock
                    self.label_to_mapindex[label] = mapindex
                    self.label_to_tlblock[label] = (btype, *lblock)
                    self.lblock_to_label[(level, hblock[-1])] = label
                    self.lblock_to_mapindex[lblock] = mapindex
                    mapindex += 1
