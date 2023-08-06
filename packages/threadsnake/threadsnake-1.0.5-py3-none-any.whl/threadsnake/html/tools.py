from typing import Dict

def tag(name:str, content:str = None, cls=None, *children, **attributes) -> str:
    result = f'<{name}'
    attributes = attributes or {}
    if cls is not None: attributes['class'] = cls
    attrib:str = ' '.join([f'{i}="{attributes[i]}"' for i in attributes])
    result += attrib
    if len(children) == 0:
        result += '/>'
    else:
        result += '>'
        for child in children:
            result += child
        result += f'</{name}>'
    return result

def link(location:str, text:str, cls:str = None):
    return tag('a', text, cls, href=location)