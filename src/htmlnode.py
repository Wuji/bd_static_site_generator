class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        prop_strings = []

        if self.props == None:
            return ""

        for prop in self.props:
            prop_strings.append( f"{prop}=\"{self.props[prop]}\"") 
        
        return " ".join(prop_strings)

    def __repr__(self):
        return f"HTMLNode(t:{self.tag}, v:{self.value}, c:{self.children}, p:{self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

        if self.value == None:
            raise ValueError("All Leaf Nodes require a value")
            
    def to_html(self):
        

        if self.tag == None:
            return self.value

        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"

        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag == None:
            raise ValueError("All Leaf Nodes require a value")
        if children == None or children == []:
            raise ValueError("ParentNodes should have children")
        
        super().__init__(tag, None, children, props=props)

    def to_html(self):
        children_text = ""

        for child in self.children:
            children_text += child.to_html()
        
        return f"<{self.tag}>{children_text}</{self.tag}>"
