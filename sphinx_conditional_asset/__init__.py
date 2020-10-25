"""Conditionally add assets in Sphinx."""

import os
from pathlib import Path
from types import MethodType
from collections.abc import Callable

__version__ = "0.0.1"


def add_js_file_conditional(
    self, filename: str, condition: [Callable, None], **kwargs
) -> None:
    """Conditionally add a js file if `condition` returns True for a page.

    Overrides the Sphinx `add_js_file` and adds an extra `condition` kwarg.
    """
    self.add_js_file(filename, **kwargs)
    self.config.conditional_script_files[filename] = condition


def add_css_file_conditional(
    self, filename: str, condition: [Callable, None], **kwargs
) -> None:
    """Conditionally add a css file if `condition` returns True for a page.

    Overrides the Sphinx `add_css_file` and adds an extra `condition` kwarg.
    """
    self.add_css_file(filename, **kwargs)
    self.config.conditional_css_files[filename] = condition


def check_conditional_assets(app, pagename, templatename, context, doctree):
    """Loop through any conditional assets and exclude if needed."""
    for path, condition in app.config.conditional_script_files.items():
        if not condition(app, pagename, templatename, context, doctree):
            context["script_files"] = [
                ii for ii in context["script_files"] if path not in ii
            ]

    for path, condition in app.config.conditional_css_files.items():
        if not condition(app, pagename, templatename, context, doctree):
            context["css_files"] = [ii for ii in context["css_files"] if path not in ii]


def setup(app):
    app.connect("html-page-context", check_conditional_assets)
    app.config["conditional_script_files"] = {}
    app.config["conditional_css_files"] = {}

    app.add_js_file_conditional = MethodType(add_js_file_conditional, app)
    app.add_css_file_conditional = MethodType(add_css_file_conditional, app)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
