import unittest

from blocktype import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode
from leafnode import LeafNode
from utilitymethods import extract_markdown_images, extract_markdown_links, extract_title, markdown_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_node_to_html_node, text_to_textnodes
from parentnode import ParentNode
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_code(self):
        text = "```\nThis is a code block\n```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a _code block_ word", TextType.TEXT)
        node3 = TextNode("This is text with a **code block**", TextType.TEXT)
        node4 = TextNode("This is text with a `code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        nodesplus = split_nodes_delimiter([node2], "_", TextType.ITALIC)
        nodesplusplus = split_nodes_delimiter([node3], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                        ])
        self.assertEqual(nodesplus, [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.ITALIC),
                            TextNode(" word", TextType.TEXT),
                        ])
        self.assertEqual(nodesplusplus, [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.BOLD),
                        ])
        self.assertRaises(Exception, split_nodes_delimiter, [node4], "`", TextType.CODE)

    def test_empty_string(self):
        text = ""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_leaf(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')
        self.assertNotEqual(node, node2)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        self.assertListEqual(extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            ),[("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_title(self):
        self.assertEqual(extract_title(markdown="# This is a title"), "This is a title")
        self.assertRaises(ValueError, extract_title, markdown="## This is a title")
        self.assertRaises(ValueError, extract_title, markdown="This is a title")

    def test_heading(self):
        text = "# This is a heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_markdown_paragraph_to_html(self):
        md = "This is a paragraph"
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), "<div><p>This is a paragraph</p></div>")

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = """
This is **bolded** paragraph



"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
            ],
        )

    def test_mixed_list(self):
        text = "- Item 1\n1. Item 2"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_multiple_parentnodes(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("p", [parent_node])
        self.assertEqual(
            parent_node2.to_html(), "<p><div><span>child</span></div></p>"
        )

    def test_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.BOLD, "None")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)

    def test_none(self):
        parent_node = ParentNode(None, None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_none(self):
        node2 = LeafNode("p", None)
        self.assertRaises(ValueError, node2.to_html)

    def test_not(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text ", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_ordered_list(self):
        text = "1. Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED)

    def test_paragraph(self):
        text = "This is a paragraph."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

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

    def test_props_to_html(self):
        node = HTMLNode("div", "Hello World", None, {"class": "text"})
        self.assertEqual(node.props_to_html(), ' class="text"')

    def test_quote(self):
        text = "> This is a quote"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_repr(self):
        node = HTMLNode("div", "Hello World", None, {"class": "text"})
        self.assertEqual(repr(node), "HTMLNode(div, Hello World, None, {'class': 'text'})")

    def test_single_line(self):
        text = "This is a single line."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [link](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ])

    def test_to_html_with_attributes(self):
    # Test with attributes
        node = HTMLNode("a", "Click me", None, {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click me</a>')

    def test_to_html_with_children(self):
        # Test with child nodes
        child = HTMLNode("span", "Child text", None, {})
        parent = HTMLNode("div", "", [child], {})
        self.assertEqual(parent.to_html(), "<div><span>Child text</span></div>")

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

    def test_to_html(self):
        # Setup - create a node with known properties
        node = HTMLNode("p", "Test content", None, {})
        
        # Test
        result = node.to_html()
        
        # Assert
        self.assertEqual(result, "<p>Test content</p>")

    def test_type(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text ", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_unordered_list(self):  
        text = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED)

if __name__ == "__main__":
    unittest.main()