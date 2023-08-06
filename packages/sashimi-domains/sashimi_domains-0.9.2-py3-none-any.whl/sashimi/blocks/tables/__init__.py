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

import re

import pandas as pd

from ..util import sorted_hierarchical_block_index
from ..annotations import (
    get_xblock_yblocks_elements,
    get_subxblocks_yblocks_elements,
    get_xblock_xelements,
    make_get_title,
    load_annotations,
)
from .tables_html import (
    html_output,
    html_multi_xblocks_yblocks_table,
    html_domain_documents_table,
    html_xblock_yblocks_table,
)
from .tables_plots import get_time_plot


def subxblocks_report(
    corpus, xbtype, xlevel, xb, ybtype, ylevel=1, *, outfile=None, plots=False
):
    """
    Produces a table reporting on the topic assemblages for each subxblock
    of `xb`.
    """
    labels = make_labels(corpus.lblock_to_label, get_labels(corpus))
    sub_annotations = load_annotations(
        corpus, get_subxblocks_yblocks_elements, xbtype, ybtype, ylevel
    )
    data = {
        "id": corpus.lblock_to_label[xlevel, xb],
        "common": sub_annotations[xlevel][xb],
    }
    if plots:
        data["plot"] = get_time_plot(corpus, xbtype, xlevel, xb)
    b_table = html_xblock_yblocks_table(data, xbtype, labels)
    sb_table = xblocks_report(
        corpus,
        xbtype,
        get_subxblocks(corpus, xbtype, xlevel, xb),
        ybtype,
        ylevel,
        plots=plots,
    )
    report = [b_table, sb_table]
    if outfile is None:
        return report
    else:
        return html_output(report, outfile)


def xblocks_report(
    corpus, xbtype, xlevel_blocks, ybtype, ylevel=1, *, outfile=None, plots=False
):
    """
    Produces a table reporting on the yblock assemblages for each xblock
    in `xhblocks`.
    """
    labels = make_labels(corpus.lblock_to_label, get_labels(corpus))
    l1_label = f"L1{xbtype[0].upper()}"
    get_title = make_get_title(corpus.col_title, corpus.col_url, corpus.col_time)
    sub_annotations = load_annotations(
        corpus, get_subxblocks_yblocks_elements, xbtype, ybtype, ylevel
    )
    annotations = load_annotations(
        corpus, get_xblock_yblocks_elements, xbtype, ybtype, ylevel
    )
    data = {}
    for xlevel, xb in xlevel_blocks:
        data[xlevel, xb] = {l1_label: {}}
        if xlevel > 1:
            data[xlevel, xb]["id"] = corpus.lblock_to_label[xlevel, xb]
            data[xlevel, xb]["common"] = sub_annotations[xlevel][xb]
            if plots:
                data[xlevel, xb]["plot"] = get_time_plot(corpus, xbtype, xlevel, xb)
        for sxlevel, sxb in get_subxblocks(corpus, xbtype, xlevel, xb, 1):
            sxdata = data[xlevel, xb][l1_label][sxb] = get_xblock_data(
                corpus,
                xbtype,
                sxlevel,
                sxb,
                ybtype,
                ylevel,
                annotations[sxlevel][sxb],
                plots=plots,
            )
            if xbtype == "doc":
                sxdata["examples"] = sxdata["examples"].agg(get_title, axis=1)

    report = html_multi_xblocks_yblocks_table(data, xbtype, labels, plots=plots)
    if outfile is None:
        return report
    else:
        return html_output(report, outfile)


def l1domain_full_report(
    corpus,
    dblock,
    ybtype,
    ylevel=1,
    *,
    outfile=None,
    plots=False,
    docs=slice(None),
    code_terms_map=None,
):
    """
    Produces a table reporting on a single domain's yblock assemblages and documents.
    """
    labels = make_labels(corpus.lblock_to_label, get_labels(corpus))
    get_title = make_get_title(corpus.col_title, corpus.col_url, corpus.col_time)
    annotations = load_annotations(
        corpus, get_xblock_yblocks_elements, "doc", ybtype, ylevel
    )
    data = get_xblock_data(
        corpus,
        "doc",
        1,
        dblock,
        ybtype,
        ylevel,
        annotations[1][dblock],
        plots=plots,
    )
    data["abstracts"] = data["examples"].loc[docs, corpus.text_sources]
    if corpus.col_venue:
        data["venues"] = data["examples"].loc[docs, corpus.col_venue]
    if code_terms_map:
        get_code_terms = make_get_code_terms(
            corpus.col_title, corpus.text_sources, code_terms_map
        )
        data["code_terms"] = data["examples"].loc[docs].agg(get_code_terms, axis=1)
    data["examples"] = (
        data["examples"].loc[docs].agg(get_title, axis=1)
    )  # must come last
    report_domain = html_xblock_yblocks_table(data, "doc", labels)
    report_contents = html_domain_documents_table(data, labels, code_terms_map)
    report = [report_domain, report_contents]
    if outfile is None:
        return report
    else:
        return html_output(report, outfile)


def get_xblock_data(
    corpus, xbtype, xlevel, xb, ybtype, ylevel, annotated, *, plots=False
):
    """
    Get the report data for the given domain.
    """
    order = "frequency" if ybtype == "doc" else "time"
    xblocks_elements = get_xblock_xelements(
        corpus, xbtype, xlevel, xb, order, ybtype=ybtype, n=None
    )
    data = {
        "id": corpus.lblock_to_label[xlevel, xb],
        "specific": annotated,
    }
    if xbtype == "doc":
        data["examples"] = corpus.data.loc[xblocks_elements]
    else:
        data["examples"] = data["examples"].map(
            lambda x: f"{x[0]} <small>({x[1]})</small>"
        )
    if plots:
        data["plot"] = get_time_plot(corpus, xbtype, xlevel, xb)

    return data


def get_codes_frequencies(corpus, dlevel, dblock, code_terms_map):
    get_code_terms = make_get_code_terms(
        corpus.col_title, corpus.text_sources, code_terms_map
    )
    domain = corpus.data.loc[corpus.dblocks[dlevel].eq(dblock)]
    domain_codes = domain.agg(get_code_terms, axis=1)
    domain_codes_cooc = domain_codes.map(tuple).value_counts()
    domain_codes_count = domain_codes.explode().value_counts()
    domain_codes_cooc.name = corpus.lblock_to_label[dlevel, dblock]
    domain_codes_count.name = corpus.lblock_to_label[dlevel, dblock]
    return domain_codes_cooc, domain_codes_count


def code_frequency_tables(corpus, domain_labels, code_terms_map):
    code_coocs_d = {}
    code_frequencies_d = {}
    for dl in domain_labels:
        cc, cf = get_codes_frequencies(
            corpus, *corpus.label_to_tlblock[dl][-2:], code_terms_map
        )
        code_coocs_d[cc.name] = cc
        code_frequencies_d[cf.name] = cf
    code_frequencies = pd.DataFrame(code_frequencies_d, dtype="Int64").fillna(0)
    code_frequencies.loc["Total"] = code_frequencies.sum().astype("Int64")
    code_frequencies["Total"] = code_frequencies.sum(axis=1).astype("Int64")
    code_coocs = pd.concat(code_coocs_d.values())
    code_coocs = code_coocs.groupby(code_coocs.index).sum()
    code_coocs.name = "Colocations"
    code_frequencies.to_csv(corpus.blocks_adir / "code_domain_frequencies.csv")
    code_coocs.to_csv(corpus.blocks_adir / "code_colocations.csv")
    

####################
# Helper functions #
####################


def get_subxblocks(corpus, xbtype, xlevel, xb, sxlevel=None):
    if sxlevel is None:
        sxlevel = xlevel - 1
    xblocks, xlevels = corpus.get_blocks_levels(xbtype)
    xblocks = xblocks[xblocks[xlevel].eq(xb)]
    return [
        corpus.hblock_to_level_block(x, xbtype)
        for x in sorted_hierarchical_block_index(xblocks, xlevels, level=sxlevel)
    ]


def make_labels(lblock_to_label, given_labels):
    def func(level, block):
        lh = lblock_to_label[level, block]
        lb = given_labels.get(lh, None)
        return lh if lb is None else f"{lh}: {lb}"

    return func


def get_labels(corpus, fpath=None):
    if (fpath is not None) and fpath.exists():
        return pd.read_csv(fpath).set_index("Domain")["Label"]
    return pd.Series(dtype=object)


def make_get_code_terms(col_title, text_sources, code_terms_map):
    code_terms_rx = {k: re.compile(rf"(?i)\b{v}\b") for k, v in code_terms_map.items()}
    text_columns = sorted(set([col_title, *text_sources]))

    def get_code_terms(row):
        code_terms = set()
        for key, rex in code_terms_rx.items():
            for text in row[text_columns]:
                if rex.search(text):
                    code_terms.add(key)
        return sorted(code_terms)

    return get_code_terms
