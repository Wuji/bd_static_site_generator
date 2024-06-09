import unittest
from main import *
from textnode import *

class TestSplitDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)

        self.assertEqual([TextNode("This is text with a ", text_type_text), TextNode("code block", text_type_code), TextNode(" word", text_type_text)], split_nodes_delimiter([node], "`", text_type_code))

class TestExtractImage(unittest.TestCase):
    def test_extract_image(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"

        self.assertEqual([("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")], extract_markdown_images(text))

class TestExtractLink(unittest.TestCase):
    def test_extract_link(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"

        self.assertEqual([("link", "https://www.example.com"), ("another", "https://www.example.com/another")], extract_markdown_links(text))

class TestSplitImage(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text)

        new_nodes = split_nodes_image([node])

        self.assertEqual([
    TextNode("This is text with an ", text_type_text),
    TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
    TextNode(" and another ", text_type_text),
    TextNode(
        "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
    )], new_nodes)

class TestSplitLing(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.example.com/second)",
            text_type_text)

        new_nodes = split_nodes_link([node])

        self.assertEqual([
    TextNode("This is text with a ", text_type_text),
    TextNode("link", text_type_link, "https://www.example.com"),
    TextNode(" and another ", text_type_text),
    TextNode(
        "second link", text_type_link, "https://www.example.com/second"
    )], new_nodes)

class TestConvertion(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"

        expected_list = [
    TextNode("This is ", text_type_text),
    TextNode("text", text_type_bold),
    TextNode(" with an ", text_type_text),
    TextNode("italic", text_type_italic),
    TextNode(" word and a ", text_type_text),
    TextNode("code block", text_type_code),
    TextNode(" and an ", text_type_text),
    TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
    TextNode(" and a ", text_type_text),
    TextNode("link", text_type_link, "https://boot.dev"),
        ]

        new_nodes = text_to_textnodes(text)

        self.assertEqual(expected_list, new_nodes)

class TestMDtoBlock(unittest.TestCase):
    def test_markdown_to_blocks1(self):
        markdown_text = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is a list item\n* This is another list item"

        expected_list = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item"
        ]

        self.assertEqual(expected_list, markdown_to_blocks(markdown_text))

    def test_markdown_to_blocks2(self):
        markdown_text = "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"

        expected_list = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ]

        self.assertEqual(expected_list, markdown_to_blocks(markdown_text))

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_blocktype_heading1(self):
        text = "# this is a heading 1"

        self.assertEqual(block_type_heading, block_to_block_type(text))
    def test_block_to_blocktype_heading2(self):
        text = "## this is a heading 2"

        self.assertEqual(block_type_heading, block_to_block_type(text))
    def test_block_to_blocktype_heading3(self):
        text = "### this is a heading 3"

        self.assertEqual(block_type_heading, block_to_block_type(text))
    def test_block_to_blocktype_heading4(self):
        text = "#### this is a heading 4"

        self.assertEqual(block_type_heading, block_to_block_type(text))
    def test_block_to_blocktype_heading5(self):
        text = "##### this is a heading 5"

        self.assertEqual(block_type_heading, block_to_block_type(text))
    def test_block_to_blocktype_heading6(self):
        text = "###### this is a heading 6"

        self.assertEqual(block_type_heading, block_to_block_type(text))
    def test_block_to_blocktype_heading7(self):
        text = "####### this is not a heading"

        self.assertEqual(block_type_paragraph, block_to_block_type(text))
    def test_block_to_blocktype_code(self):
        text = "```\nOr use 3 backticks\n```"

        self.assertEqual(block_type_code, block_to_block_type(text))
    def test_block_to_blocktype_code2(self):
        text = "```\nOr use 3 backticks\n`"

        self.assertNotEqual(block_type_code, block_to_block_type(text))
    def test_block_to_blocktype_quote(self):
        text = "> First line\n> Another line\n>\n> > Nested line\n>\n> Last line"

        self.assertEqual(block_type_quote, block_to_block_type(text))
    def test_block_to_blocktype_unordered_star_list(self):
        text = "* Apples\n* Oranges\n* Pears"

        self.assertEqual(block_type_unordered_list, block_to_block_type(text))
    def test_block_to_blocktype_unordered_dash_list(self):
        text = "- Apples\n- Oranges\n- Pears"

        self.assertEqual(block_type_unordered_list, block_to_block_type(text))
    def test_block_to_blocktype_unordered_mixed_list(self):
        text = "- Apples\n* Oranges\n- Pears"

        self.assertEqual(block_type_unordered_list, block_to_block_type(text))
    def test_block_to_blocktype_unordered_invalid_list(self):
        text = "- Apples\n Oranges\n- Pears"

        self.assertEqual(block_type_paragraph, block_to_block_type(text))
    def test_block_to_blocktype_ordered_valid_list(self):
        text = "1. First\n2. Second\n3. Third"

        self.assertEqual(block_type_ordered_list, block_to_block_type(text))
    def test_block_to_blocktype_ordered_invalid_list1(self):
        text = "1. First\n4. Second\n3. Third"

        self.assertEqual(block_type_paragraph, block_to_block_type(text))
    def test_block_to_blocktype_ordered_invalid_list2(self):
        text = "1. First\nSecond\n3. Third"

        self.assertEqual(block_type_paragraph, block_to_block_type(text))
    def test_block_to_blocktype_paragraph1(self):
        text = "this is a boring paragraph"

        self.assertEqual(block_type_paragraph, block_to_block_type(text))

    def test_block_to_blocktype_paragraph2(self):
        text = "This is **bolded** paragraph"

        self.assertEqual(block_type_paragraph, block_to_block_type(text))
