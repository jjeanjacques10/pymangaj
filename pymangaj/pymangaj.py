from enum import Enum
from .mangalivre import MangaLivre
from .muitomanga import MuitoManga
from .chapmanganato import Chapmanganato
from .lermanga import LerManga

class Sources(Enum):
    MANGA_LIVRE = 'manga_livre'
    MUITO_MANGA = 'muito_manga'
    CHAPMANGANATO = 'chapmanganato'
    LER_MANGA = 'ler_manga'

class SourceFactory:
    _value_map = {
        Sources.MANGA_LIVRE: MangaLivre,
        Sources.MUITO_MANGA: MuitoManga,
        Sources.CHAPMANGANATO: Chapmanganato,
        Sources.LER_MANGA: LerManga
    }

    @staticmethod
    def get_source(value, manga_name, chapter=0):
        cls = SourceFactory._value_map[value]
        return cls(manga_name, chapter)


class pymangaj:
    
    @staticmethod
    # Get mangas by sources
    def search(manga_name, chapter, **sources):
        pages_result = []
        if(len(sources) == 0): sources = {'sources':[Sources.LER_MANGA]}
        if(len(sources['sources']) == 0): raise Exception("Invalid source")

        for source in sources['sources']:
            manga_downloader = SourceFactory.get_source(source, manga_name, chapter)
            chapter_pages = manga_downloader.search()
            pages_result += chapter_pages
        
        return pages_result

    @staticmethod
    # Get mangas titles from sources
    def search_titles(manga_name, source):
        manga_downloader = SourceFactory.get_source(source, manga_name)
        return manga_downloader.get_titles()

