# generate 5770 nodes, if possible, with minimum edge count
import random
import tqdm
from collections import Counter

with open('GraphData/train1990-1997.txt') as f:
    edge_list = f.read().splitlines()

def get_candidates(count):
    node_list = []
    size = len(edge_list)
    show_range = range(size)
    show_range = tqdm.tqdm(edge_list, total = size, ascii=True)
    first = True
    for i in show_range:
        if first:
            first = False
            continue
        nodes = i.split()
        node_list.append(int(nodes[0]))
        node_list.append(int(nodes[1]))
    nodes_above_count = set()
    node_count = Counter(node_list)
    #nodes_above = [[x,node_list.count(x)] for x in set(node_list)]
    #nodes_above = dict((x,node_list.count(x)) for x in node_list)
    for i in node_count:
        if node_count[i] > count:
            nodes_above_count.add(i)
    return nodes_above_count

files = ['GraphData/val_nodes_2edge.txt', 'GraphData/val_nodes_4edge.txt', 'GraphData/val_nodes_8edge.txt', 'GraphData/val_nodes_16edge.txt']

counts = [2,4,8,16]

for file, count in zip(files, counts):
    with open(file, 'w') as f:
        ct = 0
        candidates = get_candidates(count)
        num_nodes = len(candidates)
        num_random = min(5770,num_nodes)
        if num_random < num_nodes:
            randos = random.sample(candidates, num_random)
        else:
            randos = candidates
        for item in randos:
            f.write("%s\n" % item)
            ct += 1
            if ct > 5769:
                break
        print(count, ct)