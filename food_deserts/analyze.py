

# coding: utf-8
# Run this script to do a t-test based on the nutrients distributed food_deserts and non_food_deserts
# It operates on the post.txt.nut.US file and depends on M16 and tract_utils
# Make additions to this file for any further analysis of the .txt.nut.US data
# This file only calls functions and writes the data to the file, create all functions on M16
# In[4]:

# Analysis done 	: t-test
# Results generated : t-test_results

import sys
sys.path.append('/nethome/ssharma321/FINAL/food_deserts')
from M16 import *
from tract_utils import *


# Load the data in M16 format
print 'Loading data'
with open('/nethome/ssharma321/split_data/post.txt.nut.US','r') as f:
    lines = f.readlines()
lines = [line.strip().split('\t') for line in lines if len(line)>10]
print 'Loading data !! DONE !!'

# Now write the food deserts to the file
print 'Running t-test'
with open('t-test_results','w+') as f:    
    for nut in ['cal','cho','fib','pro','fat','sug']:
        f.write(nut+" | t : %.3f  p : %.3f \n" % t_test(lines, nut,'fd','1'))
print 'Running t-test !! DONE !!'