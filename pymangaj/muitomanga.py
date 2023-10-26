import re
import json
import requests
from bs4 import BeautifulSoup


class MuitoManga():

    def __init__(self, manga, chapter) -> None:
        self.manga = manga
        self.chapter = chapter

    def get_titles(self, manga_name):
        url = f"https://muitomanga.com/buscar?q={manga_name}"

        headers = {
            'Cookie': 'PHPSESSID=pt9g3ip57qeearso69ocvvh2lv'
        }

        response = requests.get(url, headers=headers, data={})

        soup = BeautifulSoup(response.text, 'html.parser')
        mangas = []
        i = 0
        for manga in soup.find_all("div", {"class": "anime"}):
            i = i + 1
            mangas.append([
                i,
                manga.find("a").get("href").split("/")[-1]
            ])
        return mangas


    def get_chapter(self, manga_id):
        url = f"https://muitomanga.com/ler/{manga_id}/capitulo-{self.chapter}"
        res = requests.get(url)

        if res.status_code != 200:
            raise Exception("Not found")

        return res.text


    def get_images_by_html(html):
        regex_match_images_url = re.compile(r'\["https:(.*)\]')
        str_images_url = regex_match_images_url.search(html).group()
        return json.loads(str_images_url)


    def search(self):
        mangas = self.get_titles(self.manga.replace(" ", "+"))

        if len(mangas) == 0:
            raise Exception("Manga não encontrado")

        id_manga = (mangas[0][0] - 1)
        manga_name = mangas[id_manga][1]

        chapter_html = self.get_chapter(manga_name)

        return MuitoManga.get_images_by_html(chapter_html)