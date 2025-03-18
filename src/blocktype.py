from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def block_to_block_type(text):
    if text == "":
        return BlockType.PARAGRAPH
    lines = text.splitlines()
    if re.match(r"^#{1,6} ", text):
        return BlockType.HEADING
    if text.startswith("```") and text.endswith("```"):
        return BlockType.CODE
    if all(line.startswith("> ")for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ")for line in lines):
        return BlockType.UNORDERED
    is_ordered = True
    for i, line in enumerate(lines, 1):
        if not line.startswith(f"{i}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED
    return BlockType.PARAGRAPH
def markdown_to_blocks(markdown):

    """
    Splits the markdown text into list of Text lines.
    :param markdown: The markdown text to be split
    :return: A list of lines of texts
    """
    blocks = []
    lines = markdown.split("\n\n")
    for line in lines:
        cur = line.strip()
        if cur != "":
            blocks.append(cur)
    return blocks