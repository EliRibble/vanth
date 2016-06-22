import logging

LOGGER = logging.getLogger(__name__)

class Node(): # pylint: disable=too-few-public-methods
    def __init__(self, parent, name, children=None, value=None):
        self.children   = children or []
        self.name       = name
        self.parent     = parent
        self.value      = value
        if parent:
            parent.children.append(self)

    def __getitem__(self, key):
        for child in self.children:
            if child.name == key:
                return child

    def __repr__(self):
        return "SGMLNode {} ({})".format(self.name, self.parent.name if self.parent else None)

def parse(content):
    state = 'node-content'
    buf = ''
    parent_node = None
    current_node = None
    for c in content:
        if c == '<':
            if state == 'node-content':
                if buf == '':
                    parent_node = current_node
                    LOGGER.debug("Node content was empty, setting parent node to %s", parent_node)
                if current_node:
                    current_node.value = buf
                    LOGGER.debug("Set %s to %s", current_node.name, current_node.value)
            buf = ''
            state = 'node-name'
        elif c == '>':
            if state == 'node-name':
                LOGGER.debug("Saw opening tag %s. With parent %s", buf, parent_node)
                state = 'node-content'
                current_node = Node(parent_node, buf)
                buf = ''
            elif state == 'closing-tag':
                LOGGER.debug("Saw closing tag %s", buf)
                state = 'closed-tag'
                parent_node = current_node
                while parent_node.parent and parent_node.name != buf:
                    parent_node = parent_node.parent
                parent_node = parent_node.parent
                buf = ''
                LOGGER.debug("Set new parent to %s", parent_node.name if parent_node else None)
        elif c == '/' and buf == '':
            state = 'closing-tag'
            parent_node = current_node.parent if current_node else None
        else:
            buf += c
    root = current_node or parent_node
    while root.parent:
        root = root.parent
    print(pformat(root))
    return root

def pformat(node, indent=0):
    children = '\n'.join(pformat(child, indent+1) for child in node.children)
    return "{}{}: {}{}".format('\t' * indent, node.name, node.value, "\n" + children if node.children else '')
