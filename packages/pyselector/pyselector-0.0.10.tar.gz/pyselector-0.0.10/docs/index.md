![Python](https://img.shields.io/badge/python-3670A0?style=Flat&logo=python&logoColor=ffdd54)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
# PySelector

## 🌟 About

`pyselector` is a Python wrapper for the `rofi` application, which provides a simple and efficient way to display a list of items for user selection.

## 📦 Installation

To install `pyselector`, you can use pip:

~~~sh
pip install pyselector
~~~

## 🚀 Usage

This is a simple example 

~~~python
from pyselector import Menu

rofi = Menu.rofi()
items = [
    {"name": "item0", "date": "2022-02-10", "category": "A"},
    {"name": "item1", "date": "2022-03-20", "category": "A"},
    {"name": "item2", "date": "2022-03-19", "category": "B"},
    {"name": "item3", "date": "2022-03-18", "category": "A"},
]

selection, code = rofi.prompt(
    items=items,
    case_sensitive=False,
    multi_select=False,
    prompt="PyExample> ",
)
print(">Selected:", selection)
~~~
