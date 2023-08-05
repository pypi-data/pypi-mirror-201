# example.py
from __future__ import annotations

import functools
import logging
from typing import TYPE_CHECKING
from typing import Optional

from pyselector import Menu

if TYPE_CHECKING:
    from pyselector.key_manager import Keybind

items = [
    {"name": "item0", "date": "2022-02-10", "category": "A"},
    {"name": "item1", "date": "2022-03-20", "category": "A"},
    {"name": "item2", "date": "2022-03-19", "category": "B"},
    {"name": "item3", "date": "2022-03-18", "category": "A"},
    {"name": "item4", "date": "2022-03-21", "category": "C"},
    {"name": "item5", "date": "2022-03-20", "category": "B"},
]


def sort_by_key(key: str, items: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(items, key=lambda x: x[key])


def parse_selection(menu: Menu, keycode: int, **kwargs) -> Optional[Keybind]:
    for key in menu.keybind.registered_keys:
        if key.code == keycode:
            logging.info("keybind: %s", key)
            return key
    return None


def main() -> int:
    Menu.logging_debug(verbose=True)
    menu = Menu.rofi()

    menu.keybind.add(
        key="alt-d",
        description="sort by date",
        callback=lambda: "date",
    )
    menu.keybind.add(
        key="alt-t",
        description="sort by category",
        callback=lambda: "category",
    )
    menu.keybind.add(
        key="alt-n",
        description="sort by name",
        callback=lambda: "name",
    )

    prompt = functools.partial(
        menu.prompt, prompt="PyExample>", width="40%", height="40%"
    )

    # Enter always returns 0
    item, keycode = prompt(items=items)

    while keycode != 0:
        keybind = parse_selection(menu, keycode, item=item)
        sorted_items = sort_by_key(keybind.callback(), items=items)
        item, keycode = prompt(items=sorted_items)

    logging.info("selected: %s", item)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
