# regions is list of tuples of the form (TAG1, TAG2)
# each tag may only appear at most once among all regions

from .util import make_documentclass, render_to_png, tag_to_str, check_tag_occurs 
from . import DEFAULT_HIGHLIGHT_COLOR

def apply_code_highlighting(code, all_tags, regions_to_highlight, highlighted_wrapin):

    for tag in all_tags:
        check_tag_occurs(code, tag)

    for (from_tag, to_tag) in regions_to_highlight:
        for tag in (from_tag, to_tag):
            if not tag in all_tags:
                raise ValueError("tag %s was not registered" % (tag,))
        code = code.replace(tag_to_str(from_tag), highlighted_wrapin[0])
        code = code.replace(tag_to_str(to_tag), highlighted_wrapin[1])

    for tag in all_tags:
        code = code.replace(tag_to_str(tag), "")

    return code


def make_code_prelude(color, user_prelude):
    return "\n".join([
    r"""\usepackage{listings}
        \usepackage{xcolor}
        \usepackage{highlighter}""",
    r"""\definecolor{highlightcolor}{HTML}{""" + str(color) + r"}",
    r"""\tikzset{highlighter/.style = {highlightcolor, line width = \baselineskip}}
    """,
    user_prelude])

def render_code(
        code, all_tags, regions_to_highlight, png,
        listings_settings,
        varwidth_frac=None, color=DEFAULT_HIGHLIGHT_COLOR,
        user_prelude=""):

    (lstset, (esc_start, esc_end)) = listings_settings
    code = apply_code_highlighting(code, all_tags, regions_to_highlight,
        (esc_start + r"\HighlightFrom" + esc_end, esc_start + r"\HighlightTo{}" + esc_end))
    documentclass = make_documentclass(varwidth_frac)
    prelude = make_code_prelude(color, user_prelude)
    begindocument = r"\begin{document}"
    beginlisting = r"\begin{lstlisting}"
    endlisting = r"\end{lstlisting}"
    enddocument = r"\end{document}"

    # combine
    latex_source = "\n".join([
        documentclass,
        prelude,
        lstset,
        begindocument,
            beginlisting,
                code,
            endlisting,
        enddocument])

    render_to_png(latex_source, png)
