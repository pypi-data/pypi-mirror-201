from .file_type_utils import raw_text_from_file
import networkx as nx


def get_comments_dict(thread):

    comments_dict = dict(thread[["comment_id", "comment"]].values)
    title_id = [id for id in thread["parent_id"] if str(id).startswith("t")][0]
    title = thread["title"][0]
    comments_dict[title_id] = title

    parents_dict = dict(thread[["comment_id", "parent_id"]].values)
    num_ids_dict = {k:i for i,k in enumerate(comments_dict.keys())}

    comments_dict = {num_ids_dict[k]: v for k,v in comments_dict.items()}
    parents_dict = {num_ids_dict[k]: num_ids_dict[v] for k, v in parents_dict.items()}

    return comments_dict, parents_dict


def make_graph_from_arg_dicts(nodes_dict, relations_list):

    G = nx.DiGraph(rankdir="TB")

    for i in nodes_dict.keys():
        G.add_node(i)
    
    for rel in relations_list:
        G.add_edge(rel["from"], rel["to"], label=rel["relation"])

    attrs = {}

    for i, text in nodes_dict.items():
        attrs[i] = {"text": text}

    nx.set_node_attributes(G, attrs)

    return G    

def make_arg_dicts_from_graph(G):
    nodes = G.nodes()
    nodes_dict = {k: v["text"] for k, v in nodes.items()}
    edges = G.edges()
    labels = [G.get_edge_data(*e)["label"] for e in edges]
    edge_dicts = [{"from":e[0], "to":e[1], "relation": l} for e, l in zip(edges, labels)]
    return(nodes_dict, edge_dicts)

def get_node_viewpoint(node, parents_dict):
    relations = {"red", "green"}
    if node not in parents_dict:
        return "green"
    else:
        parent, relation = parents_dict[node]
        parent_viewpoint = get_node_viewpoint(parent, parents_dict)
        if relation in ["supports", "expands", 1]:
            return parent_viewpoint
        else:
            return list(relations - {parent_viewpoint})[0]

def get_perspectives_dict(nodes_dict, relations_list):

    parents_dict = {rel["from"]: (rel["to"], rel["relation"]) for rel in relations_list}
    perspectives = {}

    for n in nodes_dict:
        pers = get_node_viewpoint(n, parents_dict)
        perspectives[n] = pers
    return perspectives