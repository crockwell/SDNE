# generate .1% of set for validation
import random
#num_nodes = 577669
num_nodes = 40770
num_random = 5000#int(num_nodes * .001)
randos = random.sample(range(num_nodes), num_random)
with open('GraphData/val_nodes_88.txt', 'w') as f:
    for item in randos:
        f.write("%s\n" % item)