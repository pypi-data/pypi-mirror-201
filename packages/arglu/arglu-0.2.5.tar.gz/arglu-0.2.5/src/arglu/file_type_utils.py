import json
import numpy as np
import os
import re

def load_json_file(filepath):
    with open(filepath) as pf:
        filestring = pf.readlines()[0]
        json_list = json.loads(filestring)
    return json_list

def load_jsonl(path):
    data=[]
    with open(path, 'r', encoding='utf-8') as reader:
        for line in reader:
            data.append(json.loads(line))
    return data 

def list_from_file(file_name):
    with open(file_name) as handle:
        file_lines = handle.readlines()
        return [l.strip("\n") for l in file_lines]
    
def raw_text_from_file(file_name):
    with open(file_name) as handle:
        file_lines = handle.readlines()
    file_raw = "".join(file_lines)
    return file_raw.strip("\n")


def list_to_file(file_name, list_):
    with open(file_name, "w") as handle:
        for item in list_[:-1]:
            handle.write(item + "\n")
        handle.write(list_[-1])

def list_from_files(file_names):
    file_lines = []

    for file_name in file_names:
        with open(file_name) as handle:
            file_lines.extend(handle.readlines())

    return file_lines

def save_jsonl(list_, filename):
    with open(filename, 'w') as f:
        for item in list_:
            f.write(json.dumps(item) + "\n")

def write_textgraph(file_name, links_list, node_dict=None):
    #We should put something in here to enforce acyclicity 

    with open(file_name, "w+") as out_file:
        for l in links_list:
            if type(l) == dict:
                l = [node_dict[l["from"]], l["relation"], node_dict[l["to"]]]
            if l[0] == l[2]:  # A node cannot link to itself.
                continue 
            for s in l:
                s = re.sub("\n+", "", s)
                s = str(s).strip("\n")
                out_file.write(s +"\n")
            out_file.write("\n")

def read_textgraph(file_name):
    """Reads in a txtgraph file, returns a dictionary of all nodes and another dictionary with relations"""

    file_raw = raw_text_from_file(file_name)

    relations_list = file_raw.split("\n\n")
    relations_split = [rel.split("\n") for rel in relations_list]
    try:
        assert np.mean([len(rel) for rel in relations_split]) == 3.0
    except:
        print("invalid textgraph file")
        import pdb; pdb.set_trace()

    all_relations = [rel for rel in relations_split if len(rel) == 3]

    all_nodes = list(set([r[0] for r in all_relations] + [r[2] for r in all_relations]))
    nodes_dict = {i: n for i, n in enumerate(all_nodes)}
    nodes_dict_r = {n: i for i, n in enumerate(all_nodes)}

    relations_dicts = [{"from": nodes_dict_r[rel[0]],
                        "relation": rel[1],
                        "to": nodes_dict_r[rel[2]]} for rel in all_relations]

    return nodes_dict, relations_dicts

if __name__ == "__main__":
    print("hi")
    my_list = list("abcdefgh")
    test_name = "temp.txt"
    list_to_file(test_name, my_list)
    list_2 = list_from_file(test_name)
    assert my_list == list_2
    os.remove(test_name)