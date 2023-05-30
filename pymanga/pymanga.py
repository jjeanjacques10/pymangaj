from enum import Enum
from sources.mangalivre import MangaLivre
from sources.muitomanga import MuitoManga

class Sources(Enum):
    MANGA_LIVRE = 'manga_livre'
    MUITO_MANGA = 'muito_manga'

class SourceFactory:
    _value_map = {
        Sources.MANGA_LIVRE: MangaLivre,
        Sources.MUITO_MANGA: MuitoManga
    }

    @staticmethod
    def get_source(value, manga_name, chapter):
        cls = SourceFactory._value_map[value]
        return cls(manga_name, chapter)


class pymanga:
    
    @staticmethod
    # Get mangas by sources
    def search(manga_name, chapter, **sources):
        result = []
        for source in sources['sources']:
            manga_downloader = SourceFactory.get_source(source, manga_name, chapter)
            pages = manga_downloader.search()
            result += pages
        
        return result

