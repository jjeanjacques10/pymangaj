import pytest
from unittest.mock import patch
from pymangaj.muitomanga import MuitoManga

@pytest.fixture
def mock_search_manga():
    return [[1, 'one-piece'], [2, 'naruto'], [3, 'bleach']]

@patch("requests.get")
def test_search_existing_manga(mock_get, mock_search_manga):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = '["https://example.com/image1.jpg", "https://example.com/image2.jpg"]'
    mock_search_manga_result = mock_search_manga

    with patch.object(MuitoManga, "search_manga", return_value=mock_search_manga_result):
        manga_name = "One Piece"
        chapter = 1000

        manga = MuitoManga(manga_name, chapter)
        result = manga.search()

    assert result == ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]



@pytest.fixture
def mock_get_chapter():
    return """
        <html>
            <body>
                <script>
                    var images = ["https://example.com/image1.jpg", "https://example.com/image2.jpg"];
                    document.write(JSON.stringify(images));
                </script>
            </body>
        </html>
    """


@patch("requests.get")
def test_search_nonexistent_manga(mock_get, mock_search_manga):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = ""
    mock_search_manga_result = []

    with patch.object(
        MuitoManga,
        "search_manga",
        return_value=mock_search_manga_result
    ):
        manga_name = "Nonexistent Manga"
        chapter = 1

        manga = MuitoManga(manga_name, chapter)
        with pytest.raises(Exception, match="Manga não encontrado"):
            manga.search()


@patch("requests.get")
def test_get_existing_chapter(mock_get, mock_get_chapter):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = mock_get_chapter

    manga_name = "Naruto"
    chapter = 500

    manga = MuitoManga(manga_name, chapter)
    result = manga.get_chapter(manga_name)

    assert result == mock_get_chapter


@patch("requests.get")
def test_get_nonexistent_chapter(mock_get):
    mock_get.return_value.status_code = 404

    manga_name = "One Piece"
    chapter = 9999

    manga = MuitoManga(manga_name, chapter)
    with pytest.raises(Exception, match="Not found"):
        manga.get_chapter(manga_name)


def test_parse_html_and_extract_images():
    html = """
        <html>
            <body>
                <script>
                    var images = ["https://example.com/image1.jpg", "https://example.com/image2.jpg"];
                    document.write(JSON.stringify(images));
                </script>
            </body>
        </html>
    """

    expected_result = ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]

    result = MuitoManga.get_images_by_html(html)

    assert result == expected_result
