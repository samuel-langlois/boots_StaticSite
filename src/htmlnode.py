from blocktype import BlockType, block_to_block_type, markdown_to_blocks
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        if self.tag is None:
            return self.value or ""
        
        props_html = self.props_to_html()
        open_tag = f"<{self.tag}{props_html}>"
        close_tag = f"</{self.tag}>"
        
        if self.value is not None and self.children is None:
            return f"{open_tag}{self.value}{close_tag}"
        
        if self.children is None:
            return f"{open_tag}{close_tag}"
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        return f"{open_tag}{children_html}{close_tag}"
    def props_to_html(self):
        if self.props is None:
            return ""
        propL = ""
        for prop in self.props:
            propL += f' {prop}="{self.props[prop]}"'
        return propL
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    def __eq__(self, other):
        return (self.tag == other.tag and self.value == other.value and
                self.children == other.children and self.props == other.props)
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
def markdown_to_html_node(text):
    blocks = markdown_to_blocks(text)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        # Blocktype PARAGRAPH
        if block_type == BlockType.PARAGRAPH:
            htmlnodes = text_to_children(block)
            htmlnode = HTMLNode("p", None, htmlnodes, None)
            block_nodes.append(htmlnode)

        # Blocktype HEADING
        elif block_type == BlockType.HEADING:
            level = block.count("#")
            block = block.replace("#", "")
            htmlnodes = text_to_children(block)
            htmlnode = HTMLNode(f"h{level}", None, htmlnodes, None)
            block_nodes.append(htmlnode)

        # Blocktype CODE
        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            if len(lines) > 2:
                content = "\n".join(lines[1:-1])
                text_node = TextNode(content, TextType.TEXT)
                code_node = text_node_to_html_node(text_node)
                pre_node = HTMLNode("pre", None, [code_node], None)
                block_nodes.append(pre_node)

        # Blocktype QUOTE
        elif block_type == BlockType.QUOTE:
            block = block.replace(">", "").strip()
            htmlnodes = text_to_children(block)
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