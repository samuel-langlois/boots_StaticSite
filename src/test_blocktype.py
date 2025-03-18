import unittest
from blocktype import BlockType, markdown_to_blocks, block_to_block_type

class TestBlockType(unittest.TestCase):
    def test_paragraph(self):
        text = "This is a paragraph."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    def test_heading(self):
        text = "# This is a heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
    def test_code(self):
        text = "```\nThis is a code block\n```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)
    def test_quote(self):
        text = "> This is a quote"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
    def test_unordered_list(self):  
        text = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED)
    def test_ordered_list(self):
        text = "1. Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED)
    def test_mixed_list(self):
        text = "- Item 1\n1. Item 2"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    def test_empty_string(self):
        text = ""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    def test_single_line(self):
        text = "This is a single line."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
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
if __name__ == "__main__":
    unittest.main()