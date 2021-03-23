import re
from .util import make_documentclass, render_to_png, tag_to_str, check_tag_occurs, HIGHLIGHT_COLOR

# all_regions is a list of TAGS, that must begin and end regions; the regions may not overlap

def apply_math_highlighting(math, all_regions, regions_to_highlight):
    for region in all_regions:
        check_tag_occurs(math, region)

    for region in regions_to_highlight:
        if not region in all_regions:
            raise ValueError("region %s was not registered" % (region,))

    for region in all_regions:
        if region in regions_to_highlight:
            wrapin = (r"\hlight{highlightcolor}{$", r"$}")
        else:
            wrapin = (r"\hlight{white}{$", r"$}")
        pattern = re.escape(tag_to_str(region)) + r"([\s\S]*)" + re.escape(tag_to_str(region))
        repl = wrapin[0] + r"\1" + wrapin[1]
        new_math = re.sub(pattern, repl, math)
        if new_math == math:
            raise ValueError("Failed to find and replace region %s" % (region,))
        assert new_math != math
        math = new_math

    return math

def make_math_prelude():
    return "\n".join([
    r"""
        \usepackage{xcolor}
        \usepackage{bm}
        \usepackage{algpseudocode}
        \usepackage{amsmath,amssymb}
        \algdef{SE}[DOWHILE]{Do}{doWhile}{\algorithmicdo}[1]{\algorithmicwhile\ #1}
    """,
    (r"\definecolor{highlightcolor}{HTML}{" + str(HIGHLIGHT_COLOR) + r"}"),
    r"""
        \newcommand{\hlight}[2]{\setlength{\fboxsep}{0pt}\colorbox{#1}{#2}}
    """])


def render_math(math, all_regions, regions_to_highlight, png, varwidth_frac=None):

    math = apply_math_highlighting(math, all_regions, regions_to_highlight)
    documentclass = make_documentclass(varwidth_frac)
    prelude = make_math_prelude()
    begindocument = r"\begin{document}"
    enddocument = r"\end{document}"

    # combine
    latex_source = "\n".join([
        documentclass,
        prelude,
        begindocument,
            math,
        enddocument])

    render_to_png(latex_source, png)
