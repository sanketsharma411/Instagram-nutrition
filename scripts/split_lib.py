### Importing stuff
import os,sys
#sys.path.append('C:\Users\Shweta\Desktop\CS 8903\FINAL\scripts')
sys.path.append('/nethome/ssharma321/FINAL/scripts')
from analyze_utils import *
### Function Definitions
#####################################################################
# Function to load multiple post files and combine them into one
#####################################################################
def load_split_posts(base_path,n, set_loc_time = False):
    '''
    Function to load multiple post files and combine them into one
    base_path = path of the folder which has folders numbered 0...n-1
    n = number of pieces the file has been split into

    This function skips the 0th folder for the time being, 
    so it goes from 1 to n-1

    '''
    post_dict = {}
    for i in range(1,n):
        file_name = base_path+get_full_post_file_name(i)
        print file_name
        split_dict = load_post(file_name,set_loc_time)
        post_dict.update(split_dict)
        print len(split_dict),len(post_dict)
    return post_dict

#####################################################################
# Reading all the nut_info lines into one list of lines
#####################################################################
def load_split_nut_info_lines(base_path, n):
    '''
    This function reads the split nut_info files into one big list 
    of lines.
    Each individual line is well handled by the Post.set_nut_info() method
    So first load the entire post_dict
    Then load the nut_info lines
    Then pass each line to the corresponding Post.set_nut_info method

    This function skips the 0th folder for the time being, 
    so it goes from 1 to n-1
    '''
    lines = []
    for i in range(1,n):
        file_name = base_path+get_full_post_file_name(i)+'.nut_info.txt'
        with open(file_name, 'r' ) as f:
            l = f.readlines()
            lines.extend(l)
    #print len(lines)
    return lines
#####################################################################
# Function to set the nut info for the loaded posts
#####################################################################
def set_post_dict_nut_info(post_dict, nut_info_lines):
    '''
    This function sets the nut_info
    post_dict : post_dict, loaded using the load_post function
    nut_info_lines : list of raw lines from the nut_info file
    The ref to post_dict is passed here [pass by ref]
    So this function returns same post_dict reference,
    but  the post_dict is modified directly to save the nut_info
    Even if it had returned nothing it wouldnot make diff
    but returning something and saving it fits in well in our framework
    '''
    neg_count = 0
    pos_count = 0
    for line in nut_info_lines:
        post_id = line.split('\t')[0]
        if post_id not in post_dict:
            neg_count += 1
            #print 'GHANTA',post_id
        else:
            post_dict[post_id].set_nut_info(line)
            pos_count += 1
            #print 'NICES',post_id
    #print '+',pos_count,'-',neg_count
    return post_dict

#####################################################################
# Function to extract the post_ids from list of raw post.txt lines
#####################################################################
def get_post_ids(list_of_post_lines_from_post_file):
    '''
    Function to extract the post_ids from list of raw post.txt lines
    list_of_post_lines_from_post_file = directly picked up lines from post.txt file
    '''
    post_ids = []
    for line in list_of_post_lines_from_post_file:
        post_ids.append(line.split('\t')[0].strip())
    return post_ids

#####################################################################
# Function to get the path to append to the main_path given i
#####################################################################
def get_full_post_file_name(i):
    '''
    Function to get the post_file name to append to the main_path given i
    i.e. the name and path of the post.txt file
    which needs to be appended to the base_path,
    i.e. the place where all the numbered sub-folders are saved
    '''
    return '//'+str(i)+'//'+'post_'+str(i)+'.txt'


	
	
			try:
				if line[2] != '-1':
					self.calories = float(line[4])
					self.has_nuts = True
					self.match_words = line[2].strip('"').split(';')
					self.match_ids = line[3].strip('"').split(';')
					self.sugar  = float(line[5])
					self.fat  = float(line[6])
					self.cholesterol  = float(line[7])
					self.fiber  = float(line[8])
					self.protein  = float(line[9])
			except:
				pass