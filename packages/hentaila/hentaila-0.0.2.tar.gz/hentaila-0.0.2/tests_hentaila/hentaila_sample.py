import pytest

from hentaila_site.hentaila.hentaila import Hentaila
from hentaila_site.hentaila.la_types.errors import LaPageLenError

h = Hentaila()
_hentai = "https://www3.hentaila.com/hentai-euphoria-"
_chapter = "https://www3.hentaila.com/ver/euphoria--1"


def test_hentaila_directory():
    __directory = h.directory()
    assert isinstance(__directory, list)
    assert len(__directory) > 0
    print()
    print(__directory)


@pytest.mark.xfail(raises=LaPageLenError)
def test_directory_fail_max_page():
    assert len(h.directory(15, other=True)) > 0


def test_get_hentai():
    __hentai = h.get_hentai(_hentai)
    assert len(__hentai.genres) > 0
    assert len(__hentai.chapters) > 1
    assert isinstance(__hentai.title, str)
    print()
    print(__hentai)


def test_get_recents():
    __recents = h.recents()
    assert isinstance(__recents, list)
    print()
    print(__recents)


def test_get_chapter():
    __chapter = h.get_chapter(_chapter)
    assert isinstance(__chapter, list)
    print()
    print(__chapter)
