import pytest
from unittest.mock import Mock, patch
from pymangaj.chapmanganato import Chapmanganato

@pytest.fixture
def chapmanganato():
    return Chapmanganato("naruto", 2)


@patch('requests.get')
def test_get_chapters(mock_get, chapmanganato):
    # Mock the response from requests.get
    mock_response = Mock()
    mock_response.text = '''
        <ul class="row-content-chapter">
            <li><a href="/naruto/chapter-1">Chapter 1</a></li>
            <li><a href="/naruto/chapter-2">Chapter 2</a></li>
            <li><a href="/naruto/chapter-3">Chapter 3</a></li>
        </ul>
    '''
    mock_get.return_value = mock_response
    
    chapters = chapmanganato.get_chapters("https://manganato.com/naruto")
    
    expected_chapters = {
        "1": "/naruto/chapter-1",
        "2": "/naruto/chapter-2",
        "3": "/naruto/chapter-3"
    }
    
    assert chapters == expected_chapters


@patch('requests.post')
def test_search_manga(mock_post, chapmanganato):
    # Mock the response from requests.post
    mock_response = Mock()
    mock_response.json.return_value = {
        "searchlist": [
            {"url_story": "/naruto", "title": "Manga Name"}
        ]
    }
    mock_post.return_value = mock_response
    
    mangas_found = chapmanganato.search_manga()
    
    expected_mangas_found = [
        {"url_story": "/naruto", "title": "Manga Name"}
    ]
    
    assert mangas_found == expected_mangas_found


def test_get_image_urls(chapmanganato):
    html = '''
        <div class="container-chapter-reader">
            <img src="manga_page1.jpg">
            <img src="manga_page2.jpg">
            <img src="manga_page3.jpg">
        </div>
    '''
    image_urls = chapmanganato.get_image_urls(html)
    
    expected_image_urls = [
        "manga_page1.jpg",
        "manga_page2.jpg",
        "manga_page3.jpg"
    ]
    
    assert image_urls == expected_image_urls


@patch('requests.get')
def test_get_pages(mock_get, chapmanganato):
    # Mock the response from requests.get
    mock_response = Mock()
    mock_response.text = '''
        <div class="container-chapter-reader">
            <img src="manga_page1.jpg">
            <img src="manga_page2.jpg">
            <img src="manga_page3.jpg">
        </div>
    '''
    mock_get.return_value = mock_response
    
    pages = chapmanganato.get_pages("/naruto/chapter-2")
    
    expected_pages = [
        "manga_page1.jpg",
        "manga_page2.jpg",
        "manga_page3.jpg"
    ]
    
    assert pages == expected_pages
