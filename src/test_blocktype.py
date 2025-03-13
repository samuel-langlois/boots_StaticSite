import unittest
from blocktype import BlockType, block_to_block_type

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
