from bs4 import BeautifulSoup
import os
from pathlib import Path
from shutil import copytree
from subprocess import check_call

import pytest
from sphinx.errors import ThemeError
from sphinx.testing.util import SphinxTestApp
from sphinx.testing.path import path as sphinx_path


path_tests = Path(__file__).parent


class SphinxBuild:
    def __init__(self, app: SphinxTestApp, src: Path):
        self.app = app
        self.src = src

    def build(self, assert_pass=True):
        self.app.build()
        assert self.warnings == "", self.status
        return self

    @property
    def status(self):
        return self.app._status.getvalue()

    @property
    def warnings(self):
        return self.app._warning.getvalue()

    @property
    def outdir(self):
        return Path(self.app.outdir)

    def html_tree(self, *path):
        path_page = self.outdir.joinpath(*path)
        if not path_page.exists():
            raise ValueError(f"{path_page} does not exist")
        return BeautifulSoup(path_page.read_text("utf8"), "html.parser")


@pytest.fixture()
def sphinx_build_factory(make_app, tmp_path):
    def _func(src_folder, **kwargs):
        copytree(path_tests / "sites" / src_folder, tmp_path / src_folder)
        app = make_app(
            srcdir=sphinx_path(os.path.abspath((tmp_path / src_folder))), **kwargs
        )
        return SphinxBuild(app, tmp_path / src_folder)

    yield _func


def test_build_book(sphinx_build_factory, file_regression):
    """Test building the base book template and config."""
    sphinx_build = sphinx_build_factory("base")  # type: SphinxBuild
    sphinx_build.build(assert_pass=True)

    index = sphinx_build.html_tree("index.html")
    page1 = sphinx_build.html_tree("page1.html")
    for asset in ["only_page.js", "only_page.css"]:
        assert asset in str(page1)
        assert asset not in str(index)

    for asset in ["only_index.js", "only_index.css"]:
        assert asset in str(index)
        assert asset not in str(page1)