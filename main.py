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
import numpy as np
from optparse import OptionParser
import os

if __name__ == "__main__":
    os.environ["CUDA_VISIBLE_DEVICES"] = '0'#,1,2,3'
    parser = OptionParser()
    parser.add_option("-c",dest = "config_file", action = "store", metavar = "CONFIG FILE")
    parser.add_option("-e",dest = "experiment_name", action = "store", metavar = "EXPERIMENT NAME")
    '''
    *** IF you are continuing experiment, should make experiment_name
    same as folder in patent.ini from which you are getting it! ***
    '''
    options, _ = parser.parse_args()
    if options.config_file == None:
        raise IOError("no config file specified")
    if options.experiment_name == None:
        raise IOError("no experiment file specified")
        
    config = Config(options.config_file)
    
    path = os.path.join("result", config.embedding_filename, options.experiment_name)
    try: os.makedirs(path)
    except OSError: pass
    
    train_graph_data = Graph(config.train_graph_file, config.ng_sample_ratio)
   
    if config.origin_graph_file:
        origin_graph_data = Graph(config.origin_graph_file, config.ng_sample_ratio)
        
    if config.label_file:
        train_graph_data.load_label_data(config.label_file)
    
    config.struct[0] = train_graph_data.N
        
    model = SDNE(config)
    restored = model.do_variables_init(train_graph_data)
    embedding = None   
    
    fout = open(os.path.join(path, "log.txt"),"a+")  
    model.save_model(os.path.join(path, 'epoch' + '.model'))
    with open('GraphData/future_500_node_ids.txt', 'r') as f:
        test_ids = f.readlines()
    test_ids = np.array(test_ids).astype(int)
    #test_ids = set(test_ids)
    
    epochs = int(config.start_epoch)
    batch_n = 0
    print "training SDNE..."
    while (True):
        # validate
        if epochs % config.display == 0:
            model.save_model(os.path.join(path, 'epoch' + '.model'))
            ct = 0
            embedding = None
            loss = 0
            train_graph_data.is_epoch_end = True
            while (True):
                mini_batch, en, N = train_graph_data.sample(config.batch_size, do_shuffle = False)
                loss += model.get_loss(mini_batch)
                if embedding is None:
                    embedding = model.get_embedding(mini_batch)
                else:
                    embedding = np.vstack((embedding, model.get_embedding(mini_batch))) 
                if train_graph_data.is_epoch_end:
                    break

            print "Epoch : %d loss : %.3f" % (epochs, loss)
            print >>fout, "Epoch : %d loss : %.3f" % (epochs, loss)
            if config.check_link_prediction_test:
                print >> fout, epochs, "link_prediction_test:", check_link_prediction_test(embedding, train_graph_data, origin_graph_data, config.check_link_prediction_test, test_ids)
            if config.check_reconstruction:
                print >> fout, epochs, "reconstruction:", check_reconstruction(embedding, train_graph_data, config.check_reconstruction)
            if config.check_link_prediction:
                print >> fout, epochs, "link_prediction:", check_link_prediction(embedding, train_graph_data, origin_graph_data, config.check_link_prediction)
            fout.flush()
            sio.savemat(path + '/embedding.mat',{'embedding':embedding})
        if epochs >= config.epochs_limit:
            print "exceed epochs limit terminating"
            break
        epochs += 1
        # train
        ct = 0
        
        mini_batch, en, N = train_graph_data.sample(config.batch_size)
        loss = model.fit(mini_batch)
        while not train_graph_data.is_epoch_end:
            mini_batch, en, N = train_graph_data.sample(config.batch_size)
            loss = model.fit(mini_batch)
            if en * 10 > N * ct:
                print("{}% done training epoch".format(100*en/N))
                ct += 1

    sio.savemat(path + '/embedding.mat',{'embedding':embedding})
    fout.close()
