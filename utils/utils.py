import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.multiclass import OneVsRestClassifier
import pdb

class Dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def getSimilarity(result):
    return np.dot(result, result.T)
    
def check_reconstruction(embedding, graph_data, check_index):
    def get_precisionK(embedding, data, max_index):
        print "get precisionK (recon)..."
        similarity = getSimilarity(embedding).reshape(-1)
        sortedInd = np.argsort(similarity)
        numcorr = []
        cur = 0
        count = 0
        precisionK = []
        sortedInd = sortedInd[::-1]
        print(np.shape(sortedInd))
        for ind in sortedInd:
            x = ind / data.N
            y = ind % data.N
            count += 1
            if (data.adj_matrix[x].toarray()[0][y] == 1 or x == y):
                cur += 1 
            precisionK.append(1.0 * cur / count)
            numcorr.append(cur)
            if count > max_index:
                break
        return precisionK, numcorr
        
    precisionK, numcorr = get_precisionK(embedding, graph_data, np.max(check_index))
    ret = []
    for index in check_index:
        print "precisonK (recon) [%d] %.4f . #correct %i" % (index, precisionK[index - 1], numcorr[index-1])
        ret.append(precisionK[index - 1])
    return ret

def check_link_prediction(embedding, train_graph_data, origin_graph_data, check_index):
    def get_precisionK(embedding, train_graph_data, origin_graph_data, max_index):
        print "get precisionK (LP)..."
        similarity = getSimilarity(embedding).reshape(-1)
        sortedInd = np.argsort(similarity)
        cur = 0
        count = 0
        precisionK = []
        numcorr = []
        sortedInd = sortedInd[::-1]
        print(np.shape(sortedInd))
        N = train_graph_data.N
        for ind in sortedInd:
            x = ind / N
            y = ind % N
            if (x == y or train_graph_data.adj_matrix[x].toarray()[0][y] == 1):
                continue 
            count += 1
            if (origin_graph_data.adj_matrix[x].toarray()[0][y] == 1):
                cur += 1
            precisionK.append(1.0 * cur / count)
            numcorr.append(cur)
            if count > max_index:
                break
        return precisionK, numcorr
    precisionK, numcorr = get_precisionK(embedding, train_graph_data, origin_graph_data, np.max(check_index))
    ret = []
    for index in check_index:
        print "precisonK (LP)[%d] %.4f . #correct %i" % (index, precisionK[index - 1], numcorr[index-1])
        ret.append(precisionK[index - 1])
    return ret

def check_link_prediction_test(embedding, train_graph_data, origin_graph_data, check_index, test_ids):
    def get_precisionK(embedding, train_graph_data, origin_graph_data, max_index, test_ids):
        print "get precisionK (LP test)..."
        embedding_test = embedding[test_ids,:]
        similarity = np.dot(embedding_test, embedding.T).reshape(-1) #getSimilarity(embedding).reshape(-1)
        sortedInd = np.argsort(similarity)
        cur = 0
        count = 0
        precisionK = []
        numcorr = []
        sortedInd = sortedInd[::-1]
        N = train_graph_data.N
        settest = set(test_ids)
        print(np.shape(sortedInd))
        for ind in sortedInd:
            x = ind / N
            y = ind % N
            x_new = test_ids[x]
            if (x_new == y or train_graph_data.adj_matrix[x_new].toarray()[0][y] == 1):
                continue 
            if y in settest:
                continue # we only count guesses from test set to original set
            count += 1
            if (origin_graph_data.adj_matrix[x].toarray()[0][y] == 1):
                cur += 1
            precisionK.append(1.0 * cur / count)
            numcorr.append(cur)
            if count > max_index:
                print('made it with count',count)
                break
        return precisionK, numcorr
    precisionK, numcorr = get_precisionK(embedding, train_graph_data, origin_graph_data, np.max(check_index), test_ids)
    ret = []
    for index in check_index:
        print "precisonK (LP test) [%d] %.4f . #correct %i" % (index, precisionK[index - 1], numcorr[index-1])
        ret.append(precisionK[index - 1])
    return ret
 

def check_multi_label_classification(X, Y, test_ratio = 0.9):
    def small_trick(y_test, y_pred):
        y_pred_new = np.zeros(y_pred.shape,np.bool)
        sort_index = np.flip(np.argsort(y_pred, axis = 1), 1)
        for i in range(y_test.shape[0]):
            num = sum(y_test[i])
            for j in range(num):
                y_pred_new[i][sort_index[i][j]] = True
        return y_pred_new
        
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = test_ratio)
    clf = OneVsRestClassifier(LogisticRegression())
    clf.fit(x_train, y_train)
    y_pred = clf.predict_proba(x_test)
    
    ## small trick : we assume that we know how many label to predict
    y_pred = small_trick(y_test, y_pred)
    
    micro = f1_score(y_test, y_pred, average = "micro")
    macro = f1_score(y_test, y_pred, average = "macro")
    return "micro_f1: %.4f macro_f1 : %.4f" % (micro, macro)
    #############################################


    
