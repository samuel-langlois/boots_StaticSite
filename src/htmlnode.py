class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError("to_html() not implemented")
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
Assign the proper child HTMLNode objects to the block node. I created a shared text_to_children(text) function that works for all block types. It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (think TextNode -> HTMLNode).
The "code" block is a bit of a special case: it should not do any inline markdown parsing of its children. I didn't use my text_to_children function for this block type, I manually made a TextNode and used text_node_to_html_node.
Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.
Create unit tests. Here are two to get you started:
"""
def markdown_to_html(text):
    html = ""
    return html