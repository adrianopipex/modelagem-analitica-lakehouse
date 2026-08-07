"""
Funções utilitárias para extração (scraping) de dados do site público
https://books.toscrape.com/ — um site de demonstração criado
especificamente para a prática de web scraping (não requer autenticação
e permite livremente a coleta de seus dados para fins de estudo).

Estas funções são utilizadas pelo notebook
`notebooks/01_scrape_to_volume.ipynb` para coletar os dados e
armazená-los, em formato bruto (JSON), no Volume do Unity Catalog.
Este módulo contém apenas funções — a execução acontece no notebook.
"""

import json
from datetime import date
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch_page(url: str) -> BeautifulSoup:
    """Faz o download de uma página e retorna o HTML parseado."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_book_card(card, categoria: str) -> Dict:
    """Extrai os campos de um livro a partir do card na página de listagem."""
    titulo = card.h3.a["title"]
    preco_raw = card.select_one(".price_color").text
    disponibilidade_raw = card.select_one(".availability").text.strip()
    rating_classes = card.select_one(".star-rating")["class"]
    rating_raw = [c for c in rating_classes if c != "star-rating"][0]
    href = card.h3.a["href"].replace("catalogue/", "")
    url_produto = BASE_URL + "catalogue/" + href

    return {
        "titulo": titulo,
        "preco_raw": preco_raw,
        "rating_raw": rating_raw,
        "disponibilidade_raw": disponibilidade_raw,
        "categoria": categoria,
        "url_produto": url_produto,
        "dt_coleta": date.today().isoformat(),
    }


def scrape_categoria(categoria_url: str, categoria: str, max_paginas: int = 3) -> List[Dict]:
    """Percorre as páginas de uma categoria e retorna a lista de livros encontrados."""
    livros: List[Dict] = []
    url = categoria_url

    for _ in range(max_paginas):
        soup = fetch_page(url)
        cards = soup.select("article.product_pod")
        livros.extend(parse_book_card(card, categoria) for card in cards)

        next_link = soup.select_one("li.next a")
        if not next_link:
            break
        url = url.rsplit("/", 1)[0] + "/" + next_link["href"]

    return livros


def save_raw_to_volume(livros: List[Dict], output_dir: str) -> str:
    """Grava a lista de livros coletados como um arquivo JSON no Volume.

    No Databricks, os Volumes são expostos como um sistema de arquivos
    local (FUSE), permitindo o uso direto de `open()`.
    """
    file_path = f"{output_dir}/livros.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(livros, f, ensure_ascii=False, indent=2)
    return file_path
