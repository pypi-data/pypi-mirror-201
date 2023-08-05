from pyselector import Menu

items = [
    {"name": "item0", "date": "2022-02-10", "category": "A"},
    {"name": "item1", "date": "2022-03-20", "category": "A"},
    {"name": "item2", "date": "2022-03-19", "category": "B"},
    {"name": "item3", "date": "2022-03-18", "category": "A"},
]

rofi = Menu.rofi()
selection, code = rofi.prompt(
    items=items,
    case_sensitive=False,
    multi_select=False,
    prompt="PyExample> ",
    mesg="> Welcome to PySelector"
)

print(">Selected:", selection)
