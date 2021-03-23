# tutorial_highlighter

Python package for generating PNGs of code and math with custom highlighted regions using LaTeX

## Installation

Ensure that the executables `convert` from [ImageMagick](https://imagemagick.org/index.php) and `pdflatex` are on the `PATH`.

Clone the repository, and install the Python package into your Python environment:

```
git clone git@github.com:probcomp/tutorial_highlighter.git
pip install tutorial_highlighter
```

## Usage

There are two functions provided, `render_code` and `render_math`.

### `render_code`

![Animation of code highlighting](code.gif)

### `render_math`

![Animation of math highlighting](math.gif)
