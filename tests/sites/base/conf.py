from docutils.nodes import bullet_list

# -- Project information -----------------------------------------------------

project = "Sphinx Book Theme"
copyright = "2020, Executable Book Project"
author = "Executable Book Project"

master_doc = "index"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["myst_parser", "sphinx_conditional_asset"]
html_theme = "sphinx_book_theme"


def only_with_bullet_list(app, pagename, templatename, context, doctree):
    if doctree and doctree.traverse(bullet_list):
        return True


def only_on_some_pages(app, pagename, templatename, context, doctree):
    if pagename.startswith("page"):
        return True


def setup(app):
    app.add_js_file_conditional("only_index.js", only_with_bullet_list)

    app.add_js_file_conditional("only_page.js", only_on_some_pages)

    app.add_css_file_conditional("only_index.css", only_with_bullet_list)

    app.add_css_file_conditional("only_page.css", only_on_some_pages)
