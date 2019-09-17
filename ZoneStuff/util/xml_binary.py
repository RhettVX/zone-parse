from lxml.etree import Element, SubElement


def element_section(parent: Element, name: str) -> Element:
    return SubElement(parent, 'section', name=name)


def element_int(parent: Element, x: int, name: str) -> Element:
    return SubElement(parent, 'int', x=str(x), name=name)


def element_float(parent: Element, x: float, name: str) -> Element:
    return SubElement(parent, 'float', x=str(x), name=name)


def element_string(parent: Element, x: str, name: str) -> Element:
    return SubElement(parent, 'string', x=x, name=name)


def element_bytes(parent: Element, x: bytes, name: str) -> Element:
    return SubElement(parent, 'bytes', length=str(len(x)), x=''.join([f'{y:02x}' for y in x]), name=name)

# def element_pair(parent: Element, pair, name: str) -> Element:
#     print(pair)
#     # return SubElement(parent, 'pair', key=pair., value=str(value), name=name)
