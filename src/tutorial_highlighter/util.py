import subprocess
import shlex
import os
import tempfile

def make_documentclass(varwidth_frac):
    varwidth_opt = "" if varwidth_frac == None else "varwidth=" + str(varwidth_frac) + r"\linewidth"
    opts = [r"crop=true", r"border={20pt 0pt 0pt 0pt}", varwidth_opt]
    return r"\documentclass[" + ",".join(opts) + r"]{standalone}"

def check_output_and_print(cmd):
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    print("\n%s\n" % (output,))

def render_to_png(latex_source, png):
    (fd, path) = tempfile.mkstemp(suffix=".tex", text=True, dir=os.getcwd())
    with open(fd, 'w') as f:
        f.write(latex_source)
    check_output_and_print("pdflatex %s" % (shlex.quote(path),))
    check_output_and_print("pdflatex %s" % (shlex.quote(path),))
    check_output_and_print("pdflatex %s" % (shlex.quote(path),))
    pdf = path[:-4] + ".pdf"
    check_output_and_print("convert -colorspace RGB -density 500 -quality 100 %s %s" % (shlex.quote(pdf), shlex.quote(png)))
    for suffix in [".log", ".tex", ".aux", ".pdf"]:
        os.remove(shlex.quote(path[:-4] + suffix))

TAG_BOUNDARIES = (r"(*", r"*)")

def tag_to_str(tag):
    return TAG_BOUNDARIES[0] + tag + TAG_BOUNDARIES[1]

def check_tag_occurs(code, tag):
    if code.find(tag_to_str(tag)) == -1:
        raise ValueError("code does not contain tag %s" % (tag,))
