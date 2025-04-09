"""
    Split the markdown into blocks (you already have a function for this)

Loop over each block:
    Determine the type of block (you already have a function for this)

    Based on the type of block, create a new HTMLNode with the proper data
    
    Assign the proper child HTMLNode objects to the block node.
    I created a shared text_to_children(text) function that works for all block types. 
    It takes a string of text and returns a list of HTMLNodes that represent the inline 
    markdown using previously created functions (think TextNode -> HTMLNode).

    The "code" block is a bit of a special case: it should not do any inline markdown 
    parsing of its children. I didn't use my text_to_children function for this block 
    type, I manually made a TextNode and used text_node_to_html_node.
    Make all the block nodes children under a single parent HTML node 
    (which should just be a div) and return it.
    Create unit tests. Here are two to get you started:
"""
import re
from blocktype import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType


def markdown_to_html_node(text):
    blocks = markdown_to_blocks(text)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        # Blocktype PARAGRAPH
        if block_type == BlockType.PARAGRAPH:
            block_with_spaces = block.replace("\n", " ")
            htmlnodes = text_to_children(block_with_spaces)
            htmlnode = HTMLNode("p", None, htmlnodes, None)
            block_nodes.append(htmlnode)

        # Blocktype HEADING
        elif block_type == BlockType.HEADING:
            level = block.count("#")
            block = block.replace("#", "").strip()
            htmlnodes = text_to_children(block)
            htmlnode = HTMLNode(f"h{level}", None, htmlnodes, None)
            block_nodes.append(htmlnode)

        # Blocktype CODE
        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            if len(lines) > 2:
                content = "\n".join(lines[1:-1]) + "\n"
                code_node = HTMLNode("code", None, [LeafNode(None,content)], None)
                pre_node = HTMLNode("pre", None, [code_node], None)
                block_nodes.append(pre_node)

        # Blocktype QUOTE
        elif block_type == BlockType.QUOTE:
            # Split into quote lines, remove '> ' from each
            lines = block.split("\n")
            stripped_lines = [line.lstrip("> ").strip() for line in lines if line.startswith(">")]
            # Join lines while preserving line breaks
            content = "\n".join(stripped_lines)
            htmlnodes = text_to_children(content)
            htmlnode = HTMLNode("blockquote", None, htmlnodes, None)
            block_nodes.append(htmlnode)

        # Blocktype UNORDERED
        elif block_type == BlockType.UNORDERED:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                if item.strip():
                    content = item.lstrip("- ").strip()
                    children = text_to_children(content)
                    li_node = HTMLNode("li", None, children, None)
                    li_nodes.append(li_node)
            htmlnode = HTMLNode("ul", None, li_nodes, None)
            block_nodes.append(htmlnode)

        # Blocktype ORDERED
        elif block_type == BlockType.ORDERED:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                if item.strip():
                    content = item.lstrip("0123456789. ").strip()
                    children = text_to_children(content)
                    li_node = HTMLNode("li", None, children, None)
                    li_nodes.append(li_node)
            htmlnode = HTMLNode("ol", None, li_nodes, None)
            block_nodes.append(htmlnode)
    return HTMLNode("div", None, block_nodes, None)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

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
    for old_node in old_nodes:
        # Skip non-TEXT nodes - they're already formatted
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Split the text by delimiter
        split_text = old_node.text.split(delimiter)
        
        # If no delimiter was found, just add the original node
        if len(split_text) == 1:
            new_nodes.append(old_node)
            continue
            
        # Check for valid pairing (must have odd number of elements)
        if len(split_text) % 2 == 0:
            raise Exception(f"Invalid markdown syntax: Unmatched delimiter {delimiter}")
            
        # Process each piece of text
        for i, text in enumerate(split_text):
            if text == "":
                continue  # Skip empty strings but don't return
                
            if i % 2 == 0:  # Outside delimiters - regular text
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:  # Inside delimiters - apply special formatting
                new_nodes.append(TextNode(text, text_type))
    
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

def extract_title(markdown):
    """
    Extracts the title from the markdown text.
    Assumes the title is the first line that starts with a "#".
    :param markdown: The markdown text
    :return: The title as a string
    :raises ValueError: If no title is found
    """
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found in the markdown text.")

