from lxml.etree import Element, SubElement


def element_section(parent: Element, name: str) -> Element:
    return SubElement(parent, 'section', name=name)


def element_int(parent: Element, value: int, name: str) -> Element:
    return SubElement(parent, 'int', value=str(value), name=name)


def element_rgba(parent: Element, r: int, g: int, b: int, a: int, name: str) -> Element:
    return SubElement(parent, 'rgba', r=str(r), g=str(g), b=str(b), a=str(a), name=name)


def element_float(parent: Element, value: float, name: str) -> Element:
    return SubElement(parent, 'float', value=str(value), name=name)


def element_string(parent: Element, value: str, name: str) -> Element:
    return SubElement(parent, 'string', value=value, name=name)


def element_bool(parent: Element, value: bool, name: str) -> Element:
    return SubElement(parent, 'bool', value=str(value).lower(), name=name)


def element_bytes(parent: Element, value: bytes, name: str) -> Element:
    return SubElement(parent, 'bytes', length=str(len(value)), value=' '.join([f'{y:02x}' for y in value]), name=name)

# def element_pair(parent: Element, pair, name: str) -> Element:
#     print(pair)
#     # return SubElement(parent, 'pair', key=pair., value=str(value), name=name)
