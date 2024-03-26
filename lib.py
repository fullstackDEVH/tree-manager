import json


class Node:
    def __init__(self, name="root", type="folder", path=""):
        self.name = name
        self.type = type
        self.path = path
        self.children: list[Node] = []

    def add_children(self, child):
        self.children.append(child)

    def get_relative_path(self) -> str:
        return self.path


class MAryTree:
    def __init__(self, root_name="root"):
        self.root = Node(root_name)

    def find_node(self, name, node=None) -> Node | None:
        if node is None:
            node = self.root
        if node.name == name:
            return node
        for child in node.children:
            result = self.find_node(name, child)
            if result is not None:
                return result
        return None

    def add_node(self, parent_name: str, child_node: Node):
        # tham chiếu đến nút con trong seft.root
        parent_node = self.find_node(parent_name)
        if parent_node is not None:
            if parent_node.type == "folder":
                parent_node.add_children(child_node)
            else:
                print(f"{parent_name} is a file, cannot add.")
        else:
            print(f"Parent folder {parent_name} not found.")

    def delete_node_same_level1(self, target_path: list[str], node: Node = None):
        if node is None:
            node = self.root

        if len(target_path) == 0:
            return

        for child in node.children:
            if child.get_relative_path() == target_path[0]:
                if child in node.children:
                    node.children.remove(child)
                    target_path.pop(0)
                    self.delete_node_same_level(target_path, node)

        for child in node.children:
            self.delete_node_same_level(target_path, child)

    def delete_node_same_level(self, target_path: list[str], node: Node = None):
        if node is None:
            node = self.root
        if len(target_path) > 0:
            for child in node.children:
                if child.get_relative_path() in target_path:
                    if child in node.children:
                        node.children.remove(child)
                        target_path.remove(child.path)
                        self.delete_node_same_level(target_path, node)
                else:
                    self.delete_node_same_level(target_path, child)

    def display_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        print("**********")
        print(level)
        print(node.name)
        print(node.path)

        for child in node.children:
            self.display_tree(child, level + 1)

    def dict_to_node(data):
        node = Node(data["name"], data["type"])
        return node


def main():
    file_system = MAryTree()
    with open("fake_data.json", "r") as file:
        data = json.load(file)

    def add_nodes(node_data, parent_name, path=""):
        current_node_name = node_data["name"]
        path = f"{path}/{current_node_name}"
        new_node = Node(current_node_name, node_data["type"], path)

        file_system.add_node(parent_name, new_node)
        for child_data in node_data.get("children", []):
            add_nodes(child_data, current_node_name, path)

    add_nodes(data, "root")

    # node = file_system.find_node("File 11.1221")
    # print(node)
    # file_system.delete_node(
    #     [
    #         "/images/images_2/images_22.png",
    #         "/images/images_2/images_2.png",
    #     ]
    # )

    file_system.delete_node_same_level(
        [
            "/images/images_2/images_22.png",
            "/images/images_2/images_2.png",
            "/images/images_1",
        ]
    )
    file_system.display_tree()


if __name__ == "__main__":
    main()
