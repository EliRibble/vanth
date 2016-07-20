import xml.etree.ElementTree


def parse_child(element):
    values = {child.tag: child.text for child in element}
    values['id'] = element.attrib['id']
    return values

def parse(data):
    root = xml.etree.ElementTree.fromstring(data)
    assert root.tag == 'institutions'
    return [parse_child(element) for element in root]
