from enum import Enum
import re

from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE =  "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode("b", text_node.text)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode("i", text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode("code", text_node.text)
        elif text_node.text_type == TextType.LINK:
            if text_node.url is None:
                raise ValueError("Link text must have a url")
            return LeafNode("a", text_node.text, props = {"href": text_node.url})
        elif text_node.text_type == TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("Image text must have a url")
            return LeafNode("img", "",props = {"src": text_node.url, "alt": text_node.text})
        else:
            raise ValueError(f"Unsupported TextType: {text_node.text_type}")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        curText = node.text.split(delimiter)
        if len(curText) % 2 == 0:
            raise Exception("Invalid Markdown syntax")
        for x in range(0,len(curText)):
            if curText[x] ==  "":
                return new_nodes
            if x % 2 != 0:
                new_nodes.append(TextNode(curText[x], text_type))
            else:
                new_nodes.append(TextNode(curText[x], TextType.TEXT))
        
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
