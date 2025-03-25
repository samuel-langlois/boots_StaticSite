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
