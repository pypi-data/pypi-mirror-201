import os
import os.path as op
import numpy as np
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (15,5)
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from .file_type_utils import read_textgraph
from .graph_processing import make_graph_from_arg_dicts, make_arg_dicts_from_graph, get_perspectives_dict
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout




def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class bc:
    HEADER = '\033[95m'
    RED = "\u001b[31m"
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class GraphPlotter():
    def __init__(self):
        self.components_dict = {"Premise": {"abbrv": "P", "col": bc.RED, "graph_col": "red"},
                                "Claim": {"abbrv": "C", "col": bc.OKBLUE, "graph_col": "blue"},
                                "MajorClaim": {"abbrv": "MC", "col": bc.HEADER, "graph_col": "pink"},
                                "O": {"abbrv": "O", "col": bc.ENDC, "graph_col": "black"}}
  
    def draw_graph_and_print_paragraph(self, *args, node_size=5_000, font_size=50, arrowsize=20, arrowstyle='fancy'):
        return draw_graph_and_print_paragraph(*args, components_dict = self.components_dict, node_size=node_size, font_size=font_size, arrowsize=20, arrowstyle='fancy')


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]




def print_annotated_paragraph(arg_components, component_names, components_dict={}):
    format_string = ""

    compcounts = defaultdict(int)

    for comp, name in zip(arg_components, component_names):
        compcounts[name] += 1
        format_string += components_dict[name]["col"]
        format_string += f"[{components_dict[name]['abbrv']}{compcounts[name]} "
        format_string += comp
        format_string +=  " ]"
        format_string += bc.ENDC

    split_lines = list(chunks(format_string.split(" "), 20))

    format_string = "\n".join([" ".join(l) for l in split_lines]) 
    


    print(format_string)


def draw_graph_and_print_paragraph(paragraph, components, edges, link_types, components_dict={}, node_size=5_000, font_size=50, arrowsize=20, arrowstyle='fancy'):
    draw_graph(paragraph, components, edges, link_types, components_dict=components_dict, node_size=node_size, font_size=font_size, arrowsize=20, arrowstyle='fancy')
    print_annotated_paragraph(paragraph, components, components_dict=components_dict)



def convert_model_output_to_plottable_output(graph_representation):
    
    ADU_inds = graph_representation["ADU_inds"]
    text_tokenized = graph_representation["text"].split(" ")
    paragraph = [" ".join(text_tokenized[idx[0]: idx[1]]) for idx in ADU_inds]
    components = graph_representation["ADU_types"]
    edges = graph_representation["links"]
    link_types = graph_representation["link_types"]

    return (paragraph, components, edges, link_types)


def remove_colons(nx_graph):
    for n in nx_graph.nodes:
        keys = list(nx_graph.nodes[n].keys())
        for k in keys:
            nx_graph.nodes[n][k] = str(nx_graph.nodes[n][k]).replace(":","")
    return nx_graph



class GraphGenerator():
    """TODO: make this class more readable"""
    
    def __init__(self, graph, colour_map =None, title=None):
        self.graph = graph                
        self.colour_map = colour_map
     #   self.graphs = [0] * len(self.threads_lists)
        
        self.title = title
#       xzklcmzcx
     
    
    def show(self):
        self.fig, self.axis = plt.subplots()

        if self.title:
            self.axis.set_title(self.title)
            
        self.draw_graph()
    
        #self.fig.canvas.mpl_connect('key_press_event', self.key_event)
        self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
        plt.subplots_adjust(top=0.8, right=0.8)

        plt.show()
        
        
    def update_annot(self, ind):
        # print(ind)
        ind = ind["ind"][0]
        node_name = list(self.graph.nodes())[ind]

        xy = self.positions[node_name]
        self.annot.xy = xy
        self.annot.xytext=(0,0)
        

        node_attr = {'node': node_name}
        node_attr.update(self.graph.nodes[node_name])

        comment_text = node_attr["text"]
        if len(comment_text) > 200:
            comment_text = comment_text[:200] + "..."
            
        tokenized = comment_text.split(" ")
        comment_lines = []
        while len(tokenized) > 0:
            comment_lines.append("")
            while len(comment_lines[-1]) < 40:
                if len(tokenized) == 0:
                    break
                next_word = tokenized.pop(0)
                comment_lines[-1] = comment_lines[-1] + " " + next_word
        node_attr["text"] = "\n".join(comment_lines)    
        text = '\n'.join(f'{k}: {v}' for k, v in node_attr.items())
        self.annot.set_text(text)        

        
    def hover(self, e):
        vis = self.annot.get_visible()
        if e.inaxes == self.axis:
            cont, ind = self.nodes.contains(e)


            if cont:
                self.update_annot(ind)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()
                
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.fig.canvas.draw_idle()        
        
        



        
    def draw_graph(self):
        
        G = self.graph
        G = remove_colons(G)
        self.positions = graphviz_layout(G, prog="dot")
        # except:
        #self.positions = nx.spring_layout(G)
        if self.colour_map:
            node_colours = [self.colour_map[k] for k in G.nodes().keys()]
        else:
            node_colours = ["gray"] * len(self.positions)

        self.nodes = nx.draw_networkx_nodes(G, self.positions, node_color=node_colours)#, node_size=node_size)
        nx.draw_networkx_labels(G, self.positions)#, font_size=font_size)
        nx.draw_networkx_edges(G, self.positions), #edgelist=edge_pairs, arrows=True, arrowsize=arrowsize, arrowstyle=arrowstyle, alpha=1)
        nx.draw_networkx_edge_labels(G, self.positions)# edge_labels=edge_labels, font_size=font_size, font_color='red')

        #plt.tight_layout()
        plt.axis("off")
            
        self.annot = self.axis.annotate("hello", xy=(10,10), xytext=(10,10),textcoords="offset points",
                                    bbox=dict(boxstyle="round", fc="w"),
                                    arrowprops=dict(arrowstyle="<-"))
        self.annot.set_visible(False)
        

def show_graph(G, show_perspectives=True):
    nd, rd = make_arg_dicts_from_graph(G)
    if show_perspectives:
        perspectives = get_perspectives_dict(nd, rd)
        gg = GraphGenerator(G, perspectives)
    else:
        gg = GraphGenerator(G)
    gg.show()


if __name__ == "__main__":

    file_names = os.listdir("textgraphs")
    # random_file = np.random.choice(file_names)
    #random_file = "This House would make the raising of business and labour standards a prerequisite for developmental"
    nodes_dicts, relations_dicts = read_txtgraph(op.join("textgraphs", random_file))

    G = make_graph_from_arg_dicts(nodes_dicts, relations_dicts)
    perspectives = get_perspectives_dict(nodes_dicts, relations_dicts)
    colour_map = [perspectives[k] for k in sorted(list(perspectives.keys()))]

    print(nodes_dicts)
    print(relations_dicts)

    assert nodes_dicts == nd

    for i in rd:
        assert i in relations_dicts
    assert len(rd) == len(relations_dicts)

    #draw_networkx_graph(G)
    gg = GraphGenerator(G, colour_map)
    gg.show()