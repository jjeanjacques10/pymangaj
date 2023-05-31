import pytest
from unittest.mock import patch
from pymangaj.mangalivre import MangaLivre

@pytest.fixture
def mock_search_manga():
    return [
        {"id_serie": 1, "name": "Naruto"},
        {"id_serie": 2, "name": "Dragon Ball"},
        {"id_serie": 3, "name": "Bakuman"}
    ]

@patch("requests.post")
def test_search_existing_manga(mock_post, mock_search_manga):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"series": mock_search_manga}

    manga_name = "Naruto"
    chapter = 100
    manga = MangaLivre(manga_name, chapter)

    result = manga.search()

    assert result is not None

@patch("requests.post")
def test_search_nonexistent_manga(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"series": []}

    manga_name = "Nonexistent Manga"
    chapter = 100
    manga = MangaLivre(manga_name, chapter)

    with pytest.raises(Exception) as e:
        manga.search()

    assert str(e.value) == "Manga não encontrado"

@patch("requests.get")
def test_get_chapter_existing(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "chapters": [
            {
                "id_serie": 1,
                "id_chapter": 90649,
                "number": "100",
                "releases": {
                    "_scan1": {
                        "id_release": 95444,
                        "link": "/ler/naruto/online/95444/100"
                    }
                }
            }
        ]
    }

    id_serie = 1
    chapter = 100
    manga = MangaLivre("Naruto", chapter)

    result = manga.get_chapter(id_serie)

    assert result == (95444, "/ler/naruto/online/95444/100")

@patch("requests.get")
def test_get_chapter_nonexistent(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "chapters": [
            {
                "number": "99",
                "releases": {}
            },
            
        ]
    }

    id_serie = 1
    chapter = 100
    manga = MangaLivre("Naruto", chapter)

    result = manga.get_chapter(id_serie)

    assert result is None

@patch("requests.get")
def test_get_key(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<script type=\"text/javascrip\">    window.READER_ID_RELEASE = \'59513\';    window.READER_DOMAIN = \'main\';    window.READER_TOKEN = \'abc123\';</script>"

    link = "/chapter/1234"
    manga = MangaLivre("Naruto", 100)

    result = manga.get_key(link)

    assert result == "abc123"
