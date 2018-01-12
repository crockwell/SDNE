'''
Reference implementation of SDNE

Author: Xuanrong Yao, Daixin wang

for more detail, refer to the paper:
SDNE : structral deep network embedding
Wang, Daixin and Cui, Peng and Zhu, Wenwu
Knowledge Discovery and Data Mining (KDD), 2016
'''

#!/usr/bin/python2
# -*- coding: utf-8 -*-



from config import Config
from graph import Graph
from model.sdne import SDNE
from utils.utils import *
import scipy.io as sio
import time
import copy


if __name__ == "__main__":
    config = Config()
    
    origin_graph_data = Graph(config.origin_file_path, config.ng_sample_ratio)
    train_graph_data = Graph(config.train_file_path, config.ng_sample_ratio)
    
    #load label for classification
    #graph_data.load_label_data(config.label_file_path)
    
    config.struct[0] = train_graph_data.N
    
    model = SDNE(config)    
    model.do_variables_init(train_graph_data, config.DBN_init)

    epochs = 0
    batch_n = 0
    
    #graph_data = graph_data.subgraph(config.sample_method, config.sample_ratio)
    
    fout = open(config.embedding_filename + "-log.txt","w") 
    while (True):
        mini_batch = train_graph_data.sample(config.batch_size)
        loss = model.fit(mini_batch)
        batch_n += 1
        print "Epoch : %d, batch : %d, loss: %.3f" % (epochs, batch_n, loss)
        if train_graph_data.is_epoch_end:
            epochs += 1
            batch_n = 0
            print "Epoch : %d loss : %.3f" % (epochs, loss)
            if epochs % config.display == 0:
                embedding = None
                while (True):
                    mini_batch = train_graph_data.sample(config.batch_size, do_shuffle = False)
                    loss += model.get_loss(mini_batch)
                    if embedding is None:
                        embedding = model.get_embedding(mini_batch)
                    else:
                        embedding = np.vstack((embedding, model.get_embedding(mini_batch)))
                
                    if train_graph_data.is_epoch_end:
                        break

                result = check_link_prediction(embedding, train_graph_data, origin_graph_data, [100,200,300,400,500,600,700,800,900,1000])
                #data = origin_data.sample(origin_data.N, with_label = True)
                #check_multi_label_classification(model.get_embedding(data), data.label)
                print >> fout, epochs, result
            if epochs > config.epochs_limit:
                print "exceed epochs limit terminating"
                break
            last_loss = loss
    embedding = model.get_embedding(origin_graph_data.sample(origin_graph_data.N, do_shuffle = False))
    sio.savemat(config.embedding_filename + '-' + '_embedding.mat',{'embedding':embedding})
    fout.close()
