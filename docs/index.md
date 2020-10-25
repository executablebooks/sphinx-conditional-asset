# sphinx-conditional-asset


```{image} https://readthedocs.org/projects/sphinx-conditional-asset/badge/?version=latest
:target: https://sphinx-conditional-asset.readthedocs.io/en/latest/?badge=latest
:alt: Documentation
```

```{image} https://img.shields.io/pypi/v/sphinx-conditional-asset.svg
:target: https://pypi.org/project/sphinx_conditional_asset
:alt: PyPi page
```

Conditionally add assets (JS and CSS) to your Sphinx build.

This package allows you to choose certain pages on which to load conditional
assets, rather than forcing you to load assets for all pages. This allows you to avoid loading scripts and CSS on pages that do not need them.
It is meant primarily for Sphinx developers, but can be used as a part of any Sphinx build.

## Install

To install `sphinx-conditional-asset` run the following command:

```
pip install git+https://executablebooks/sphinx-conditional-asset
```

and activate the extension via `conf.py`:

```python
extensions = [
    ...
    "sphinx_conditional_asset",
]
```

## Use

This package adds two new methods to the instance of `sphinx.Application` that
is provided by `setup(app)`, `app.add_js_file_conditional` and `app.add_css_file_conditional`. They take the same arguments as [`app.add_js_file`](https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_js_file) and [`app.add_css_file`](https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_css_file), along with an additional `condition` argument.

**The `condition` argument**: takes a **function** that accepts the same arguments as the [`html-page-context` Sphinx event](https://www.sphinx-doc.org/en/master/extdev/appapi.html#event-html-page-context).

When each page is loaded, the function will be called with the `html-page-context`
arguments. If it returns `True` then the asset *will* be loaded onto the page.

## Examples

For example, let's say we only wanted to load `thebe` on pages that start with
`thebe_`. To do so, we'd add this to our `setup(app)` function:

```python
def only_on_some_pages(app, pagename, templatename, context, doctree):
    if pagename.startswith("thebe_"):
        return True

def setup(app):
    app.add_js_file_conditional(
        "https://unpkg.com/thebelab@latest/lib/index.js",
        only_on_some_pages
    )
```

Here's an example that checks for an `admonition` node in the page's doctree:

```python
from sphinx_theme import ThebeButtonNode
def only_when_node_present(app, pagename, templatename, context, doctree):
    if doctree.traverse(ThebeButtonNode):
        return True

def setup(app):
    app.add_js_file_conditional(
        "https://unpkg.com/thebelab@latest/lib/index.js",
        only_when_node_present
    )
```
