from textnode import TextNode, TextType, split_nodes_images

def main():
    node = TextNode("this is stuff and things", TextType.BOLD, "https://www.boot.dev")
    print(node)
    node2 = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    print(split_nodes_images(node2))

if __name__ == "__main__":
    main()