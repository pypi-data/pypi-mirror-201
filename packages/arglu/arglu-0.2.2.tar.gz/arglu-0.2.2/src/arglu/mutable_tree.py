import networkx as nx

class MutableTree:
    def __init__(self, comments_dict):
        self.comments_dict = comments_dict

    def __getitem__(self, idx):
        return self.comments_dict[idx]

    def __iter__(self):
        comments_sorted = sorted(list(self.comments_dict.items()),
                                 key=lambda x: x[1].get_dist_from_root(self.comments_dict))
        self.comment_ids_sorted = [c[0] for c in comments_sorted]
        self.current_idx = 0
        return self

    def __next__(self):
        current_idx = self.current_idx
        if self.current_idx < len(self.comment_ids_sorted):
            self.current_idx += 1
            comment_id = self.comment_ids_sorted[current_idx]
            return comment_id, self.comments_dict[comment_id]
        else:
            raise StopIteration

    def add_node(self, idx, node):
        self.comments_dict[idx] = node

    def get_node(self, idx):
        return self.comments_dict[idx]

    def remove_node(self, idx):
        self.comments_dict.pop(idx)

    def get_higher_or_same_level_nodes(self, node):
        dist_from_root = self.comments_dict[node].get_dist_from_root(self.comments_dict)
        nodes = []
        for idx, n in self.comments_dict.items():
            if n.get_dist_from_root(self.comments_dict) <= dist_from_root:
                if not idx == node:
                    nodes.append(idx)
        return nodes

    def find_children(self, idx):
        child_ids = []
        for c in self.comments_dict.values():
            if c.parent_id == idx:
                child_ids.append(c.id)
        return child_ids

    def replace_node(self, old_idx, new_idx, new_node):

        assert self.comments_dict[old_idx].parent_id == new_node.parent_id

        old_node_children = self.find_children(old_idx)
        self.comments_dict.pop(old_idx)
        self.comments_dict[new_idx] = new_node
        for child_idx in old_node_children:
            child = self.comments_dict[child_idx]
            child.parent_id = new_idx
            self.comments_dict[child_idx] = child

    def to_networkx_graph(self):
        comments_sorted = sorted(list(self.comments_dict.items()),
                                 key=lambda x: x[1].get_dist_from_root(self.comments_dict))
        self.comment_ids_sorted = [c[0] for c in comments_sorted]
        G = nx.DiGraph(rankdir="TB")
        
        colon_trans = str.maketrans("","",":")
        
        for i, idx in enumerate(self.comment_ids_sorted):
            node = self.comments_dict[idx]
            if i == 0:
                G.add_node(idx, text=node.text.translate(colon_trans))
            else:
                G.add_node(idx, text=node.text.translate(colon_trans))
                G.add_edge(idx, node.parent_id, label=node.parent_edge_label.translate(colon_trans))

        return G