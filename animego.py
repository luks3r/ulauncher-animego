from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import lib.animego as animego
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction


@dataclass
class Anime:
    title: str
    romaji: str
    url: str
    image: str
    genre: str
    year: Optional[int]

    @classmethod
    def from_item(cls, item: animego.Item) -> Anime:
        return cls(
            title=item.Title,
            romaji=item.Romaji,
            url=item.Url,
            image=item.ImageUrl,
            genre=item.Genre or None,
            year=int_or_none(item.Year),
        )


def int_or_none(s: str) -> Optional[int]:
    try:
        return int(s)
    except ValueError:
        return None


def search_request(query: str, search_type: str = animego.All) -> list[Anime]:
    stype = search_type.lower()
    if stype not in [animego.All, animego.Anime, animego.Manga]:
        stype = animego.All
    result = animego.Search(query, stype)
    objects = [Anime.from_item(result[i]) for i in range(len(result))]
    return objects


def search(query: str, preferences: dict[str, str]) -> ExtensionResultItem:
    results = search_request(query, preferences["search_mode"])
    items = []
    for result in results:
        description = f"{result.genre} | {result.year}"
        title = (
            result.title
            if preferences["title_format"].lower() == "russian"
            else result.romaji
        )

        item = ExtensionResultItem(
            icon=result.image,
            name=title,
            description=description,
            on_enter=OpenUrlAction(result.url),
        )
        items.append(item)
    return items


if __name__ == "__main__":
    print(search("death"))
