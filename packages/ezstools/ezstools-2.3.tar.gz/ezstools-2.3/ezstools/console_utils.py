"""
Methods for console interaction
"""
# creates link to put in terminal
from typing import Any, List, Union
from pick import pick


def link(uri, label=None):
    if label is None: 
        label = uri
    parameters = ''

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)


def pickmenu(options: List[Any], title: str, indicator:str = "->", default_index: int = 0, multiple: bool = False, min_selected: int = 0) -> Union[str, int]:

    return pick(options, title, indicator = indicator, default_index = default_index, multiselect = multiple, min_selection_count = min_selected)
