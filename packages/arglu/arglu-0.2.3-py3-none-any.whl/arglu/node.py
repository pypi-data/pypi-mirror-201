class Node:
    def __init__(self, text, id, parent_id=None, node_type="comment", parent_edge_label="reply"):
        self.text = text
        self.parent_id = parent_id
        self.id = id
        self.node_type = node_type
        self.parent_edge_label = parent_edge_label

    def __str__(self):
        return f"{self.node_type}: {self.text}"

    def __repr__(self):
        return self.__str__()

    def is_root(self):
        if self.parent_id is not None:
            return False
        else:
            return True

    def get_dist_from_root(self, comments_dict):
        if self.is_root():
            return 0
        else:
            parent = comments_dict[self.parent_id]
            return 1 + parent.get_dist_from_root(comments_dict)

    def get_parent(self, comments_dict):
        return comments_dict[self.parent_id]
