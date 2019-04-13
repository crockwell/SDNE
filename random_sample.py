#!/usr/bin/env python

import numpy as np
import pandas as pd
import math
import random

random.seed(0)

# np.random.seed(0)
# 
data = pd.read_csv("full_1988_1990_with_future500.txt", delimiter=" ", header=None).values

prev_line_number = 30206

num_rows = data.shape[0]

future = data[prev_line_number:]
duplicate = [None]*(future.shape[0] - 500)
counter = 0
for i in range(future.shape[0]):
   if i == 0:
      prev_val = future[0,0]
      continue

   if future[i,0] == prev_val:
      duplicate[counter] = i
      counter += 1
   else:
      prev_val = future[i,0]

# rand_ind = np.random.randint(0,future.shape[0],int(0.85*future.shape[0]))

omit_idx = set()
counter = 0
for i in range(int(0.15*future.shape[0])):
   random_idx = random.choice(duplicate)
   while random_idx in omit_idx:
      random_idx = random.choice(duplicate)

   omit_idx.add(random_idx)
# rand_ind = np.random.randint(0,num_rows,int(0.85*num_rows))

omitted = np.zeros((future.shape[0] - len(omit_idx),2))
counter = 0
for i in range(future.shape[0]):
   if i not in omit_idx:
      omitted[counter,:] = future[i,:]
      counter += 1

# training = data[rand_ind]
np.savetxt("ommited_future.txt", omitted, delimiter=" ", fmt='%i')



10
2
# 
# rand_ind
# 


