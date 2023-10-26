# PyMangaJ

Pymangaj is a Python library for searching and retrieving manga pages from different sources. It provides a simple interface to fetch manga pages from popular manga websites.

## Installation

You can install pymangaj using pip:

``` bash
pip install pymangaj
```

## Getting Started

### Search Pages

To use pymangaj, import the `pymangaj` module and call the `search()` method. Pass the manga name, chapter, and the sources you want to search from as arguments. The method will return a list of manga pages.

``` python
from pymangaj import pymangaj, Sources

pymangaj.search("Naruto", 1, sources=[Sources.CHAPMANGANATO, Sources.LER_MANGA])
```

``` shell
['https://v2.mkklcdnv6tempv2.com/img/tab_2/00/13/32/ng952689/vol_72_chapter_699_the_seal_of_reconciliation/1-o.jpg', 'https://v2.mkklcdnv6tempv2.com/img/tab_2/00/13/32/ng952689/vol_72_chapter_699_the_seal_of_reconciliation/2-o.jpg'...]
```

### Search Titles

Import the `pymangaj` module and call the `search_titles`()` method. Pass the manga name you want to search. The method will return a list of manga titles.

``` python
from pymangaj import pymangaj, Sources

pymangaj.search_titles("Naruto", source=Sources.LER_MANGA)
```

``` shell
[{'title': 'Naruto: Konoha Shinden &#8211; Yukemuri Ninpouchou', 'url': 'https://lermanga.org/mangas/naruto-konoha-shinden-yukemuri-ninpouchou/'}, {'title': 'Naruto Gaiden: Uzu no Naka no Tsumujikaze', 'url': 'https://lermanga.org/mangas/naruto-gaiden-uzu-no-naka-no-tsumujikaze/'}]
```

## Sources

pymangaj supports the following manga sources:

|          Source                       | Language | Status  |    Source     |
| ------------------------------------- | -------- | ------  |  ----------   |
| [MangaLivre](https://mangalivre.net/) |   PT-BR  |   ❌   |  MANGA_LIVRE   |
| [MuitoManga](https://muitomanga.com/) |   PT-BR  |   ❌   |  MUITO_MANGA   |
| [Manganato](https://manganato.com/)   |   EN-US  |   ✅   |  CHAPMANGANATO |
| [LerManga](https://lermanga.org/)     |   PT-BR  |   ✅   |  LER_MANGA     |

## License

This project is licensed under the [MIT License](./LICENSE). See the LICENSE file for details.

## Contribution

Contributions to pymangaj are welcome! If you have any bug reports, feature requests, or suggestions, please open an issue on the [GitHub repository](https://github.com/jjeanjacques10/pymangaj).

## Authors

- [@jjeanjacques10](https://github.com/jjeanjacques10)

## Contributors

- [@fabiobarkoski](https://github.com/fabiobarkoski)
