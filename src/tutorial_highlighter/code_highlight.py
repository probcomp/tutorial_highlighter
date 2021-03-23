# regions is list of tuples of the form (TAG1, TAG2)
# each tag may only appear at most once among all regions

from .util import make_documentclass, render_to_png, tag_to_str, check_tag_occurs, HIGHLIGHT_COLOR

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


def make_code_prelude():
    return "\n".join([
    r"""
        \usepackage{listings}
        \usepackage{textcomp}
        \usepackage{xcolor}
        \usepackage{bm}
        \usepackage{highlighter}""",
    (r"\definecolor{highlightcolor}{HTML}{" + str(HIGHLIGHT_COLOR) + r"}"),
    r"""
        \definecolor{boldkwcolor}{HTML}{00679e}
        \tikzset{highlighter/.style = {highlightcolor, line width = \baselineskip}}
    """])

def get_listings_settings():
    lstset = r"""
    \lstset{
      escapeinside={(@*}{*@)},
      basicstyle=\ttfamily\small,
      numbers=left,
      columns=fullflexible,
      keepspaces=true,
      literate={~} {$\sim$}{1},
      %upquote=true,
      % Define . and % and @ as letters to include them in keywords.
      %alsoletter={\.},%,\.,\%,\#, \@, \?, \/, \~, !},
      alsoletter={!?-,.@},
      % First type of keywords.
      % Use \bfseries\textcolor{OliveGreen} to get bolded text.
      morekeywords=[1]{function, if, else, end, while, for, begin, in, const, struct, return},
      keywordstyle=[1]\textcolor{brown},
      % Second type of keywords.
      % Use \bfseries\textcolor{OliveGreen} to get bolded text.
       morekeywords=[2]{\@gen, \@trace,Gen\.importance, Gen\.simulate,Gen\.update,Gen\.metropolis_hastings,Gen\.maybe_resample!},
      keywordstyle=[2]\textcolor{boldkwcolor},
      % Add strings
      showstringspaces=False,
      %stringstyle=\ttfamily\color{NavyBlue},
      stringstyle=\ttfamily\bfseries\color{red},
      morestring=[b]{"},
      morestring=[b]{'},
      % l is for line comment
      morecomment=[l]{\#},
      commentstyle=\color{gray}\ttfamily}"""
    escapeinside = (r"(@*", r"*@)")
    return (lstset, escapeinside)

def render_code(code, all_tags, regions_to_highlight, png, listings_settings=get_listings_settings(), varwidth_frac=None):
    (lstset, (esc_start, esc_end)) = listings_settings
    code = apply_code_highlighting(code, all_tags, regions_to_highlight,
        (esc_start + r"\HighlightFrom" + esc_end, esc_start + r"\HighlightTo{}" + esc_end))
    documentclass = make_documentclass(varwidth_frac)
    prelude = make_code_prelude()
    #listing_settings = get_listing_settings()
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
