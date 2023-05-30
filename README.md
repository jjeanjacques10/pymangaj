# PyManga

PyManga is a Python library for searching and retrieving manga pages from different sources. It provides a simple interface to fetch manga pages from popular manga websites.

## Installation

You can install PyManga using pip:

``` bash
pip install pymanga
```

## Getting Started

To use PyManga, import the `pymanga` module and call the `search()` method. Pass the manga name, chapter, and the sources you want to search from as arguments. The method will return a list of manga pages.

``` python
from pymanga import pymanga, Sources

pymanga.search("Naruto", 1, sources=[Sources.MANGA_LIVRE, Sources.MUITO_MANGA])
```

## Sources

PyManga supports the following manga sources:

|          Source                       | Language | Status | 
| ------------------------------------- | -------- | ------ | 
| [MangaLivre](https://mangalivre.net/) |   PT-BR  |   ✅   | 
| [MuitoManga](https://muitomanga.com/) |   PT-BR  |   ✅   | 

## License

This project is licensed under the [MIT License](./LICENSE). See the LICENSE file for details.

## Contribution

Contributions to PyManga are welcome! If you have any bug reports, feature requests, or suggestions, please open an issue on the [GitHub repository](https://github.com/jjeanjacques10/pymanga).

## Authors

- [@jjeanjacques10](https://github.com/jjeanjacques10)