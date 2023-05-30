import re

import requests

headers = {
    'authority': 'mangalivre.net',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
    'cache-control': 'max-age=0',
    'cookie': '_ga=e88959f7-3144-4ae1-af76-cc99b0df6e80; __cf_bm=9SAugMSkcEA8uS.y5FOZY3v.0aNn9ixEZPjsM2iSsP0-1665619463-0-Aa+7SXgc7e2OpVQtzIm4aZ1YSXqEz3CXssnfWO+zBj1yG+g21hUjq8u++ogPiGr0NsHH7kKPUHHmQ8ezanE581oEECXcKvZJjK3vx/FgdoQ/zjLBoyEmVvFfKu+rX16jiw==; cf_use_ob=0',
    'referer': 'https://mangalivre.net/ler/naruto/online/70908/700-09',
    'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42'
}

headers_2 = {
        'authority': 'mangalivre.net',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '_ga=e88959f7-3144-4ae1-af76-cc99b0df6e80; __cf_bm=5KDbO1NiKCprQ4ALceOr5UTG7B1n2U4tZ.19Fskp1os-1665617107-0-AYqASKEgB0jSGmmoLUnqambiOQwd4gxR17TEWSoslp2twJ6U1oFj+5PRkZkwGmCyJ+LI61LAFCiQKnu0z9k0XsP3iTmSsVrhSaMLbLFJfS/vjg5l3nqZtNTuNydyN1ceLA==; cf_use_ob=0',
        'origin': 'https://mangalivre.net',
        'referer': 'https://mangalivre.net/lista-de-mangas/ordenar-por-numero-de-leituras/todos/desde-o-comeco',
        'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'Access-Control-Allow-Origin': '*',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42',
        'x-requested-with': 'XMLHttpRequest'
    }

class MangaLivre:

    def __init__(self, manga_name, chapter) -> None:
        self.manga_name = manga_name
        self.chapter = chapter

    def search_manga(self, name):
        url = "https://mangalivre.net/lib/search/series.json"

        payload = f"search={name}"
     
        response = requests.post(url, headers=headers_2, data=payload)

        return response.json().get("series")


    def get_chapter(self, id_serie, page=1):
        url = f"https://mangalivre.net/series/chapters_list.json?page={page}&id_serie={id_serie}"
    
        headers = {
            'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://mangalivre.net/manga/naruto/1',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42',
            'sec-ch-ua-platform': '"Linux"'
        }

        try:
            response = requests.request("GET", url, headers=headers, data={})
            if response.status_code == 200:
                for chapter in response.json().get('chapters'):
                    if chapter.get('number') == str(self.chapter):
                        release_scan = list(chapter.get("releases").keys())[0]
                        return chapter.get("releases").get(release_scan).get("id_release"), chapter.get("releases").get(
                            release_scan).get("link")
                return self.get_chapter(id_serie, page + 1)
        except Exception as e:
            Exception(f"Error finding chapter {self.chapter} - {e}")


    def get_key(self, link):
        url = f"https://mangalivre.net{link}"
        response = requests.get(url, headers=headers, data={})
        key_trash = re.findall(r'window\.READER_TOKEN = \'(.+)\';', response.text)
        key = key_trash[0]
        return key


    def get_page(self, id_release, key):
        url = f"https://mangalivre.net/leitor/pages/{id_release}.json?key={key}"
        response = requests.get(url, headers=headers, data={})
        pages = []
        for page in response.json().get("images"):
            pages.append(page.get("legacy"))
        return pages


    def search(self):
        mangas = self.search_manga(self.manga_name)
        if not mangas:
            raise Exception("Manga não encontrado")

        id_serie = mangas.pop(0).get("id_serie")
        id_release, link = self.get_chapter(id_serie)
        
        key = self.get_key(link)
        return self.get_page(id_release, key)