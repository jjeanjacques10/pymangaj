import pytest
from unittest.mock import patch, MagicMock
from pymangaj import pymangaj, Sources
from pymangaj.mangalivre import MangaLivre
from pymangaj.muitomanga import MuitoManga

@pytest.fixture
def mock_manga_livre_search():
    mock_search = MagicMock(return_value=["MangaLivre Page 1", "MangaLivre Page 2"])
    MangaLivre.search = mock_search
    return mock_search

@pytest.fixture
def mock_muito_manga_search():
    mock_search = MagicMock(return_value=["MuitoManga Page 1", "MuitoManga Page 2"])
    MuitoManga.search = mock_search
    return mock_search

def test_search_manga_livre(mock_manga_livre_search):
    manga_name = "Naruto"
    chapter = 100
    sources = [Sources.MANGA_LIVRE]

    result = pymangaj.search(manga_name, chapter, sources=sources)

    assert result == ["MangaLivre Page 1", "MangaLivre Page 2"]
    mock_manga_livre_search.assert_called_once_with()

def test_search_muito_manga(mock_muito_manga_search):
    manga_name = "One Piece"
    chapter = 200
    sources = [Sources.MUITO_MANGA]

    result = pymangaj.search(manga_name, chapter, sources=sources)

    assert result == ["MuitoManga Page 1", "MuitoManga Page 2"]
    mock_muito_manga_search.assert_called_once_with()

def test_search_multiple_sources(mock_manga_livre_search, mock_muito_manga_search):
    manga_name = "Dragon Ball"
    chapter = 50
    sources = [Sources.MANGA_LIVRE, Sources.MUITO_MANGA]

    result = pymangaj.search(manga_name, chapter, sources=sources)

    assert result == ["MangaLivre Page 1", "MangaLivre Page 2", "MuitoManga Page 1", "MuitoManga Page 2"]
    mock_manga_livre_search.assert_called_once_with()
    mock_muito_manga_search.assert_called_once_with()

def test_search_no_sources(mock_manga_livre_search, mock_muito_manga_search):
    manga_name = "Bleach"
    chapter = 300
    sources = []

    with pytest.raises(Exception) as e:
            pymangaj.search(manga_name, chapter, sources=sources)

    assert str(e.value) == "Invalid source"
    mock_manga_livre_search.assert_not_called()
    mock_muito_manga_search.assert_not_called()

def test_search_zero_sources(mock_manga_livre_search, mock_muito_manga_search):
    manga_name = "Bleach"
    chapter = 300

    result = pymangaj.search(manga_name, chapter)

    assert result == ["MangaLivre Page 1", "MangaLivre Page 2"]
    mock_manga_livre_search.assert_called_once_with()