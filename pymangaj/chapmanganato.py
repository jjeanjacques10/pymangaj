import re
import requests
from bs4 import BeautifulSoup

headers = {
    "authority": "manganato.com",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://manganato.com",
    "referer": "https://manganato.com/",
    "sec-ch-ua": '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57",
    "x-requested-with": "XMLHttpRequest"
}

class Chapmanganato:

    def __init__(self, manga_name, chapter) -> None:
        self.manga_name = manga_name
        self.chapter = chapter


    def get_chapters(self, manga_url):
        response = requests.get(manga_url, data="", headers=headers)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        chapter_list = soup.find('ul', class_='row-content-chapter')
        chapters = chapter_list.find_all('li')

        chapter_links = [chapter.a['href'] for chapter in chapters]
        chapter_numbers = [{re.findall(r'\d+$|\D+$|\d+.\d+$', link)[0]: link} for link in chapter_links]
        
        merged_dict = {key: value for d in chapter_numbers for key, value in d.items()}

        return merged_dict


    def search_manga(self):
        url = "https://manganato.com/getstorysearchjson"

        payload = f"searchword={self.manga_name}"


        response = requests.post(url, data=payload, headers=headers)
        mangas_found = response.json()['searchlist']

        return mangas_found
    

    def get_image_urls(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        image_urls = []
        
        # Find all <img> tags within the <div> with class "container-chapter-reader"
        img_tags = soup.select('div.container-chapter-reader img')
        
        # Extract the 'src' attribute from each <img> tag
        for img in img_tags:
            url = img.get('src')
            if url:
                image_urls.append(url)
        
        return image_urls


    def get_pages(self, chapter):
        response = requests.get(chapter, data="", headers=headers)
        return self.get_image_urls(response.text)


    def search(self):
        mangas = self.search_manga()
        if not mangas:
            raise Exception("Manga não encontrado")

        manga_url = mangas[0]['url_story'].replace("\/","/")
        chapters = self.get_chapters(manga_url)

        chapter = chapters[str(self.chapter)]

        return self.get_pages(chapter)