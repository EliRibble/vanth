import vanth.sgml


def child_values(node):
    return [(child.name, child.value) for child in node.children]

def test_siblings():
    result = vanth.sgml.parse("<A><B><C>1<D>2<E>3</B></A>")
    assert result.name == 'A'
    assert child_values(result['B']) == [('C', '1'), ('D', '2'), ('E', '3')]

def test_closing():
    result = vanth.sgml.parse("<A><B><C>1</B><D><E>2</D></A>")
    assert result.name == 'A'
    assert child_values(result) == [('B', ''), ('D', '')]
    assert child_values(result['B']) == [('C', '1')]
    assert child_values(result['D']) == [('E', '2')]
