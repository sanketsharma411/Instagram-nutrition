import sys, urllib
sys.path.append('C:\Users\Shweta\Desktop\CS 8903\FINAL\scripts')
from InstaLib import *
from analyze_utils import *
from match_utils import *
from random import shuffle, randint
import numpy as np
################################################################################
# Loading the post file
################################################################################
post_file = 'C:\Users\Shweta\Desktop\CS 8903\FINAL\Data\sample_post.txt'
post_dict = load_post(post_file)
################################################################################
# Loading the nut info
################################################################################
nut_info_path = 'C:\\Users\\Shweta\\Desktop\\CS 8903\\FINAL\\results\\'
nut_info_file_name_list = ['hit_2_step_1.txt','hit_direct.txt','miss.txt']
# Reading the file into the system memory
lines = []
for file_name in nut_info_file_name_list :
    with open(nut_info_path+file_name,'r') as f:
        lines.extend(list(f))
count = 0
################################################################################
#                    Now Actually setting the nut info
################################################################################
for line in lines:
    post_dict[line.split('\t')[0]].set_nut_info(line)
    count += 1
    if not count%1000:
        print count
################################################################################
################################################################################
# ############################# IT WORKS ##################################### #
################################################################################
################################################################################
#                Getting the  median calories info
################################################################################
l = []
has_nuts= 0
# Computing the median calories, and creating a 
for post_id in post_dict.keys():
    if post_dict[post_id].has_nuts:
        has_nuts += 1
        l.append(float(post_dict[post_id].calories))
med = np.median(np.array(l))
avg = sum(l)/has_nuts

for post_id in post_dict:
    post_dict[post_id].set_cal_class(post_dict[post_id].calories > med)

count  = 0
l = []
for post_id in post_dict:
    if post_dict[post_id].loc != 0:
        l.append(post_dict[post_id].loc.split(','))

################################################################################
############# Set comment info with open()
################################################################################
lines = read_lines('C:\Users\Shweta\Desktop\CS 8903\FINAL\Data\sample_comments.txt')
print 'Setting the comments'
for line in lines:
    post_dict[line.split('\t')[0]].set_comment(line)
    

    
    



 


