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

        text_list = node.text.split(delimiter)
        if len(text_list) % 2 == 0:
            raise Exception("Invalid Markdown syntax")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        for x in range(0,len(text_list)):
            if text_list[x] ==  "":
                return new_nodes
            if x % 2 != 0:
                new_nodes.append(TextNode(text_list[x], text_type))
            else:
                new_nodes.append(TextNode(text_list[x], TextType.TEXT))
        
    return new_nodes
"""
Extracts markdown images from a given text using regex find all
:param text: The text to extract images from
:return: A list of tuples containing the image alt text and the image URL
"""
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    if old_nodes == []:
        return []
    new_nodes = []
    
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        
        if not images:
            new_nodes.append(old_node)
            continue
            
        remaining_text = old_node.text
        
        for image_alt, image_url in images:
            image_markdown = f"![{image_alt}]({image_url})"
            parts = remaining_text.split(image_markdown, 1)
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            remaining_text = parts[1] if len(parts) > 1 else ""
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

"""
Extracts markdown links from a given text using regex find all
:param text: The text to extract links from
:return: A list of tuples containing the link text and the link URL
"""
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_link(old_nodes):
    if old_nodes == []:
        return []
    new_nodes = []

    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)

        if not links:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        for link_alt, link_url in links:
            link_markdown = f"[{link_alt}]({link_url})"
            parts = remaining_text.split(link_markdown, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))

            remaining_text = parts[1] if len(parts) > 1 else ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    """
    Splits the text into TextNode objects based on the delimiters for bold, italic, and code.
    :param text: The text to be split
    :return: A list of TextNode objects
    """
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes