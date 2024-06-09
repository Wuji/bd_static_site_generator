from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type == "text":
            if not old_node.text.count(delimiter) % 2 == 0:
                raise Exception(f"Invalid Markdown: no matching end for: '{delimiter}'")
            parts = old_node.text.split(delimiter)
            odd = True
            for part in parts:
                if odd == True and not part == "":
                    new_list.append(TextNode(part, text_type_text))
                    odd = not odd
                else:
                    new_list.append(TextNode(part, text_type))
                    odd = not odd

        else:
            new_list.append(old_node)

    return new_list


def split_nodes_image(old_nodes):
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type == "text":
            text = old_node.text
            images = extract_markdown_images(text)
            if len(images) == 0:
                new_list.append(old_node)
                continue
            for image in images:

                left, right = text.split(f"![{image[0]}]({image[1]})", 1)

                if not left == "":
                    new_list.append(TextNode(left, text_type_text))

                new_list.append(TextNode(image[0], text_type_image, image[1]))

                text = right
            if not text == "":
                new_list.append(TextNode(text, text_type_text))
        else:
            new_list.append(old_node)

    return new_list

def split_nodes_link(old_nodes):
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type == "text":
            text = old_node.text
            links = extract_markdown_links(text)
            if len(links) == 0:
                new_list.append(old_node)
                continue
            for link in links:

                left, right = text.split(f"[{link[0]}]({link[1]})", 1)

                if not left == "":
                    new_list.append(TextNode(left, text_type_text))

                new_list.append(TextNode(link[0], text_type_link, link[1]))

                text = right
            if not text == "":
                new_list.append(TextNode(text, text_type_text))
        else:
            new_list.append(old_node)


    return new_list


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def text_to_textnodes(text):
    text_node = TextNode(text, text_type_text)
    new_nodes = []

    new_nodes.append(text_node)

    # print(f"bolds: {split_nodes_delimiter(new_nodes, text_delimiter_bold, text_type_bold)}")
    new_nodes = split_nodes_delimiter(new_nodes, text_delimiter_code, text_type_code)
    new_nodes = split_nodes_delimiter(new_nodes, text_delimiter_bold, text_type_bold)
    new_nodes = split_nodes_delimiter(new_nodes, text_delimiter_italic, text_type_italic)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown):
    return markdown.split("\n\n")

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "uo_list"
block_type_ordered_list = "o_list"


def block_to_block_type(markdown_block):

    # Headings: Start with 1-6 # followed by a space and then Text
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    # Code blocks must start with 3 backticks and end with 3 backticks.
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return block_type_code
    # qote block starts with >
    if all(list(map(lambda x: x.startswith(">"), markdown_block.split("\n")))):
        return block_type_quote
    # unordered list starts with * or -
    if all(list(map(lambda x: x.startswith(("* ", "- ")), markdown_block.split("\n")))):
        return block_type_unordered_list
    # ordered list starts with number followed by . Number must start with 1 and increment by 1 for each line
    ordered = False
    list_lines = markdown_block.split("\n")
    for i in range(0, len(list_lines)):
        if list_lines[i].startswith(f"{i+1}. "):
            ordered = True
        else:
            ordered = False
            break
    if ordered:
        return block_type_ordered_list
    # othwise normal paragraph
    return block_type_paragraph


def main():
    # TODO Extract into texts
    # print(TextNode("This is a text node", "bold", "https://www.boot.dev"))
    print("----Main----")

if __name__ == "__main__":
    main()
