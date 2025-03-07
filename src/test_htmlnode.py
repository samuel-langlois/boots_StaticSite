import unittest

from htmlnode import HTMLNode


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
    def test_none(self):
        node = HTMLNode("div", "Hello World", None, None)


if __name__ == "__main__":
    unittest.main()