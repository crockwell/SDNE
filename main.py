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
    
    #tt = time.ctime().replace(' ','-')
    path = os.path.join("result", config.embedding_filename, options.experiment_name)
    try: os.makedirs(path)
    except OSError: pass
    
    train_graph_data = Graph(config.train_graph_file, config.ng_sample_ratio)
   
    if config.origin_graph_file:
        origin_graph_data = Graph(config.origin_graph_file, config.ng_sample_ratio)
        
    if config.label_file:
        #load label for classification
        train_graph_data.load_label_data(config.label_file)
    
    config.struct[0] = train_graph_data.N
        
    model = SDNE(config)
    restored = model.do_variables_init(train_graph_data) # takes 40 mins per epoch (per layer?)
    # only need to do this once -- once model loaded is fixed.
    embedding = None
    
    if not restored:
        print('generating embeddings for epoch 0...')
        ct = 0
        while (True):
            mini_batch, en, N = train_graph_data.sample(config.batch_size, do_shuffle = False)
            if embedding is None:
                embedding = model.get_embedding(mini_batch)
            else:
                embedding = np.vstack((embedding, model.get_embedding(mini_batch))) 
            if train_graph_data.is_epoch_end:
                break
            if en * 10 > N * ct:
                print(en/N*100,"% done embedding")
                ct += 1
        #print(np.shape(embedding))

        print('saving model from epoch 0...')
        fout = open(os.path.join(path, "log.txt"),"a+")  
        model.save_model(os.path.join(path, 'epoch' + str(0) + '.model'))
        sio.savemat(os.path.join(path, 'embedding.mat'),{'embedding':embedding})
        
    epochs = int(config.start_epoch)
    batch_n = 0
    print "training SDNE..."
    while (True):
        ct = 0
        while not train_graph_data.is_epoch_end:
            mini_batch, en, N = train_graph_data.sample(config.batch_size)
            loss = model.fit(mini_batch)
            if en * 10 > N * ct:
                print(en/N*100,"% done training epoch")
                ct += 1
        loss = 0
        if epochs % config.display == 0: # should probably change this to be 5 or something -- very slow!
            embedding = None
            ct = 0
            while (True):
                mini_batch, en, N = train_graph_data.sample(config.batch_size, do_shuffle = False)
                loss += model.get_loss(mini_batch)
                if embedding is None:
                    embedding = model.get_embedding(mini_batch)
                else:
                    embedding = np.vstack((embedding, model.get_embedding(mini_batch))) 
                if train_graph_data.is_epoch_end:
                    break
                if en * 10 > N * ct:
                    print(en/N*100,"% done embedding")
                    ct += 1
                    
            print('embed shape',np.shape(embedding))

            print "Epoch : %d loss : %.3f" % (epochs, loss)
            print >>fout, "Epoch : %d loss : %.3f" % (epochs, loss)
            if config.check_reconstruction:
                print >> fout, epochs, "reconstruction:", check_reconstruction(embedding, train_graph_data, config.check_reconstruction)
            if config.check_link_prediction:
                print >> fout, epochs, "link_prediction:", check_link_prediction(embedding, train_graph_data, origin_graph_data, config.check_link_prediction)
            if config.check_classification:
                data, en, N = train_graph_data.sample(train_graph_data.N, do_shuffle = False,  with_label = True)
                print >> fout, epochs, "classification", check_multi_label_classification(embedding, data.label)
            fout.flush()
            model.save_model(os.path.join(path, 'epoch' + str(epochs) + '.model'))
            sio.savemat(path + '/embedding.mat',{'embedding':embedding})
        if epochs >= config.epochs_limit:
            print "exceed epochs limit terminating"
            break
        epochs += 1

    sio.savemat(path + '/embedding.mat',{'embedding':embedding})
    fout.close()
