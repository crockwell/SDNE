# SDNE
This repository adopts implementation of *SDNE* by [suanrong](https://github.com/suanrong/SDNE) as described in the paper:<br>
> Structural Deep network Embedding.<br>
> Daixin Wang, Peng Cui, Wenwu Zhu<br>
> Knowledge Discovery and Data Mining, 2016.<br>
> <Insert paper link>

The *SDNE* algorithm learns a representation for nodes in a graph, and do link prediction and reconstruction. Please check the [paper](http://www.kdd.org/kdd2016/subtopic/view/structural-deep-network-embedding) for more details. Our version is adapted to make future predictions on the [Patent Citation Network](http://www.cs.cmu.edu/~jure/pubs/powergrowth-kdd05.pdf) in addition to normal reconstruction and in-set predictions. Some small changes are made to speed up computation. It is compatable with python2. Our code is modified slightly to run with a GPU. Multiple CPUs (and GPU) are recommended due to memory and time constraints. The model requires tensorflow, version 1.4 was tested.

### Basic Usage on patent citation graph
```
$ python main.py -c config/patent.ini -e <experiment_name>
```
>modify config file to tune hyperparameters or change dataset

### Input
Input graph data is a **txt** file under **GraphData folder**. A small subset (1988-1989, inclusive) of the Patent Citation Network is included
#### file format
The txt file should be **edgelist** and **the first line** should be **N** , the number of vertexes and **E**, the number of edges

#### files
Origin graph file contains all edges while train graph file has 15% of edges missing and is used for training.
train_graph_file = GraphData/omitted_1988_1990_with_future500.txt
origin_graph_file = GraphData/full_1988_1990_with_future500.txt

Files are saved in sparse form.

#### txt file sample
	5242 14496
	0 1
	0 2
	4 9
	...
	4525 4526

> noted: The nodeID starts from 0.<br>
> noted: The graph should be an undirected graph, so if (I  J) exist in the Input file, (J  I) should not.

#### patent.ini details
to restore a model on a given epoch, change the following lines:
restore_model = ./result/patent/<model_name>/epoch.model
start_epoch = xx
Pretrained model is not included because of size.

The following lines can change batch size, loss weight, and hidden and embedding size
struct = -1,400,40 # hidden & embedding size 

;the loss func is  // gamma * L1 + alpha * L2 + reg * regularTerm //
alpha = 100
gamma = 1
reg = 1

;the weight balanced value to reconstruct non-zero element more.
beta = 10
        
batch_size = 16
epochs_limit = 100
learning_rate = 0.01

dbn_init = True
dbn_epochs = 200
dbn_batch_size = 64
dbn_learning_rate = 0.1

#### Model overview
The main train / test loop occurs in main.py. It calls utils/utils.py for evaluation. Models are in model/rbm.py and model/sdne.py, and graph operations are in graph.py. Both reconstruction and link prediction are measured.

### Citing
If you find *SDNE* useful in your research, we ask that you cite the following paper:

	@inproceedings{Wang:2016:SDN:2939672.2939753,
	 author = {Wang, Daixin and Cui, Peng and Zhu, Wenwu},
	 title = {Structural Deep Network Embedding},
	 booktitle = {Proceedings of the 22Nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining},
	 series = {KDD '16},
	 year = {2016},
	 isbn = {978-1-4503-4232-2},
	 location = {San Francisco, California, USA},
	 pages = {1225--1234},
	 numpages = {10},
	 url = {http://doi.acm.org/10.1145/2939672.2939753},
	 doi = {10.1145/2939672.2939753},
	 acmid = {2939753},
	 publisher = {ACM},
	 address = {New York, NY, USA},
	 keywords = {deep learning, network analysis, network embedding},
	} 



