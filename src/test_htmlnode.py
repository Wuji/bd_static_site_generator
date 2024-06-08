import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "this is my value", [], {"href": "https://www.google.com", "target": "_blank"} )
        
        self.assertEqual(
            'href="https://www.google.com" target="_blank"', node.props_to_html()
        )

    def test_repr(self):
        node = HTMLNode("a", "this is my value", [], {"href": "https://www.google.com", "target": "_blank"} )
        self.assertEqual(
            "HTMLNode(t:a, v:this is my value, c:[], p:{'href': 'https://www.google.com', 'target': '_blank'}", repr(node)
        )

class TestLeafNode(unittest.TestCase):
    def test_to_html1(self):
        node = LeafNode("p", "This is a paragraph of text.")
        
        self.assertEqual(
            '<p>This is a paragraph of text.</p>', node.to_html()
        )

    def test_to_html2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        
        self.assertEqual(
            '<a href="https://www.google.com">Click me!</a>', node.to_html()
       )

    def test_no_tag(self):
        node = LeafNode(None, "I am a boring text")

        self.assertEqual(
            "I am a boring text", node.to_html()
        )

class TestParentNode(unittest.TestCase):
    def test_to_html1(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        
        self.assertEqual(
            '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>', node.to_html()
        )
        
if __name__ == "__main__":
    unittest.main()
