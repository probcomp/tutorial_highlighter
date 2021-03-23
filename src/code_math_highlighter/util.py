import os
import tempfile

HIGHLIGHT_COLOR = "ffe70f"

def make_documentclass(varwidth_frac):
    varwidth_opt = "" if varwidth_frac == None else "varwidth=" + str(varwidth_frac) + r"\linewidth"
    opts = [r"crop=true", r"border={20pt 0pt 0pt 0pt}", varwidth_opt]
    return r"\documentclass[" + ",".join(opts) + r"]{standalone}"

def render_to_png(latex_source, png):
    (fd, path) = tempfile.mkstemp(suffix=".tex", text=True, dir=os.getcwd())
    with open(fd, 'w') as f:
        print(latex_source)
        f.write(latex_source)
    os.system("pdflatex %s" % (path,))
    os.system("pdflatex %s" % (path,))
    os.system("pdflatex %s" % (path,))
    pdf = path[:-4] + ".pdf"
    os.system("convert -colorspace RGB -density 500 -quality 100 %s %s" % (pdf, png))
    for suffix in [".log", ".tex", ".aux", ".pdf"]:
        os.remove(path[:-4] + suffix)

TAG_BOUNDARIES = (r"(*", r"*)")

def tag_to_str(tag):
    return TAG_BOUNDARIES[0] + tag + TAG_BOUNDARIES[1]

def check_tag_occurs(code, tag):
    if code.find(tag_to_str(tag)) == -1:
        raise ValueError("code does not contain tag %s" % (tag,))

