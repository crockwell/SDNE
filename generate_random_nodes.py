# generate .1% of set for validation
import random
num_nodes = 577669
num_random = int(num_nodes * .001)
randos = random.sample(range(num_nodes), num_random)
with open('GraphData/val_nodes.txt', 'w') as f:
    for item in randos:
        f.write("%s\n" % item)