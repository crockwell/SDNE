#!/usr/bin/env python

import numpy as np
import pandas as pd
import math

np.random.seed(0)

data = pd.read_csv("mapped_output.dat", delimiter=" ", header=None).values

#prev_line_number = 1226658

num_rows = data.shape[0]

#future = data[prev_line_number:]
#rand_ind = np.random.randint(0,future.shape[0],int(0.85*future.shape[0]))
rand_ind = np.random.randint(0,num_rows,int(0.85*num_rows))

training = data[rand_ind]
np.savetxt("foo.txt", training, delimiter=" ", fmt='%i')


# 
# rand_ind
# 


