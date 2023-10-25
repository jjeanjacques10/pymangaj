import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse

   

headers = {
    "authority": "lermanga.org",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
    "cookie": "modoLeitura=1",
    "referer": "https://lermanga.org/capitulos/one-piece-capitulo-500/",
    "sec-ch-ua": '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99""',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61",
    "x-requested-with": "XMLHttpRequest"
}

class LerManga:

    def __init__(self, manga_name, chapter) -> None:
        self.manga_name = manga_name
        self.chapter = chapter

    def search_manga(self, name):
        url = "https://lermanga.org/wp-admin/admin-ajax.php"

        querystring = {"action":"wp-manga-search-manga","title":self.manga_name}

        payload = ""

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        mangas = []

        for manga in response.json().get("data"):
            if "url" in manga:
                mangas.append(manga)
            
        return mangas
    
    def get_chapter(self, manga_url):
        payload = ""
        response = requests.request("GET", manga_url, data=payload, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        chapters = soup.find_all('div', class_='single-chapter')

        chapter_data = []

        for chapter in chapters:
            number = chapter['data-id-cap']
            url = chapter.find('a')['href']
            chapter_data.append({
                'number': number,
                'url': url
            })

        return [d for d in chapter_data if d['number'] in self.chapter][0]
    
    def get_base_img_url_from_chapter(self, chapter_url):
        parsed_url = urlparse(chapter_url)

        path_components = parsed_url.path.split('/')

        if len(path_components) < 4:
            return None

        base_path = path_components[2]
        chapter_name = path_components[-1]

        new_path = f"/{base_path[0].upper()}/{base_path}/{chapter_name}"

        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, new_path, '', '', ''))

        new_url = new_url.replace("-capitulo-", "/capitulo-")
        new_url = new_url.replace("lermanga.org", "img.lermanga.org")

        return new_url
    
    def get_page(self, chapter_url):
        payload = ""
        response = requests.request("GET", chapter_url, data=payload, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        select = soup.find('select', class_='select_paged')
        pages = []

        base_page_url = self.get_base_img_url_from_chapter(chapter_url)

        if select:
            options = select.find_all('option')
            for option in options[1:]:  # Skip the first option
                page_number, _ = option.text.split(' / ')
                page_number = int(page_number) - 1  # Convert to 0-based index
                pages.append(f"{base_page_url}{page_number}.jpg")

        return pages


    def search(self):
        mangas = self.search_manga(self.manga_name)
        if not mangas:
            raise Exception("Manga não encontrado")
        
        manga_url = mangas[0]['url']
       
        chapter = self.get_chapter(manga_url)
        
        pages = self.get_page(chapter["url"])

        return pages
