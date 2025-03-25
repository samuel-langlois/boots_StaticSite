import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(), '<div class="container"><span>child</span></div>'
        )
    def test_none(self):
        parent_node = ParentNode(None, None)
        self.assertRaises(ValueError, parent_node.to_html)
    def test_eq(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), parent_node2.to_html())
        self.assertEqual(parent_node, parent_node2)
        parent_node3 = ParentNode("p", [child_node])
        self.assertNotEqual(parent_node, parent_node3)
    def test_multiple_parentnodes(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("p", [parent_node])
        self.assertEqual(
            parent_node2.to_html(), "<p><div><span>child</span></div></p>"
        )


if __name__ == "__main__":
    unittest.main()