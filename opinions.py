from unicodedata import normalize

import requests
from bs4 import BeautifulSoup


def get_professor_opinions(professor_name: str):
    html_doc = requests.get(
        f"https://www.nuevosemestre.com/profesor/{professor_name}"
    ).text

    soup = BeautifulSoup(html_doc, "html.parser")

    p_tags = soup.select('div[id^="opinion-"] p')

    opinions_info: list[str] = []
    for p_tag in p_tags:
        opinions_info.append(p_tag.text)

    return opinions_info


def format_profesor_name(professor_name: str):
    return (
        normalize("NFD", professor_name.lower().replace(" ", "-").replace(".", ""))
        .encode("ascii", "ignore")
        .decode("utf-8")
    )


def order_professor_opinions(
    professor_opinions: list[str],
) -> tuple[list[str], list[str]]:
    ordered_professor_opinions: tuple[list[str], list[str]] = ([], [])

    for index, value in enumerate(professor_opinions):
        if index % 2 == 0:
            ordered_professor_opinions[0].append(value)
        elif index % 2 != 0:
            ordered_professor_opinions[1].append(value)
        else:
            print("ERROR: bs.")

    return ordered_professor_opinions
