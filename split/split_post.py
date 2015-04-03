import sys
sys.path.append('/nethome/ssharma321/FINAL/scripts') 
from split_lib import *
#basepath = 'C:\Users/Shweta/Desktop/CS 8903/FINAL/split/test'
#basepath = '/nethome/ssharma321/test/split_data'
#filename = '/nethome/ssharma321/test/split_data/post.txt'
basepath = '/nethome/ssharma321/split_data_2'
filename = '/nethome/ssharma321/post_2.txt'
n = 40	
offset = 39
debug = True

split_post(basepath,filename,n,offset,debug)









