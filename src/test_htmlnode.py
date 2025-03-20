import unittest

from htmlnode import HTMLNode, markdown_to_html_node


class TestTextNode(unittest.TestCase):
    
    def test_eq(self):
        node = HTMLNode("div", "Hello World", None, {"class": "text"})
        node2 = HTMLNode("div", "Hello World", None, {"class": "text"})
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = HTMLNode("div", "Hello World", None, {"class": "text"})
        self.assertEqual(repr(node), "HTMLNode(div, Hello World, None, {'class': 'text'})")
    
    def test_to_html(self):
        node = HTMLNode("div", "Hello World", None, {"class": "text"})
        self.assertRaises(NotImplementedError, node.to_html)
        # Uncomment the following line when to_html is implemented
        #self.assertEqual(node.to_html(), '<div class="text">Hello World</div>')

    def test_props_to_html(self):
        node = HTMLNode("div", "Hello World", None, {"class": "text"})
        self.assertEqual(node.props_to_html(), ' class="text"')

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()