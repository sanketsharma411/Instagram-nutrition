### Importing stuff
import os,sys
#sys.path.append('C:\Users\Shweta\Desktop\CS 8903\FINAL\scripts')
sys.path.append('/nethome/ssharma321/FINAL/scripts')
from analyze_utils import *
### Function Definitions
#####################################################################
# Load multiple post files and combine them into one
#####################################################################
def load_split_posts(base_path,n,offset=0):
    '''
    Function to load multiple post files and combine them into one
    base_path = path of the folder which has folders numbered offset through (offset+n-1)
    n = number of pieces the file has been split into
    '''
    post_dict = {}
    for i in range(offset,offset+n):
        file_name = base_path+get_full_post_file_name(i)
        print file_name
        split_dict = load_post(file_name)
        post_dict.update(split_dict)
        print len(split_dict),len(post_dict)
    return post_dict

#####################################################################
# Extract the post_ids from list of raw post.txt lines
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
# Reading all the nut_info lines into one list of lines
#####################################################################
def load_split_nut_info_lines(base_path, n,offset=0):

    '''
    This function reads the split nut_info files into one big list 
    of lines.
    Each individual line is well handled by the Post.set_nut_info() method
    So first load the entire post_dict
    Then load the nut_info lines
    Then pass each line to the corresponding Post.set_nut_info method
    '''
    lines = []
    for i in range(offset,offset+n):
        file_name = base_path+get_full_post_file_name(i)+'.nut_info.txt'
        with open(file_name, 'r' ) as f:
            l = f.readlines()
            lines.extend(l)
    #print len(lines)
    return lines
#####################################################################
# Function to set the nut info for the loaded posts
#####################################################################
def join_nut_info_2_post_dict(post_dict, nut_info_lines):
    '''
    This function combines info from raw nut_info file to the loaded post_dict
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
# Get the path to append to the main_path given i
#####################################################################
def get_full_post_file_name(i):
    '''
    Function to get the post_file name to append to the main_path given i
    i.e. the name and path of the post.txt file
    which needs to be appended to the base_path,
    i.e. the place where all the numbered sub-folders are saved
	
	EDIT 23 Feb :  New file name //i//post.txt as opposed to 
								//i//post_i.txt
    '''
    return '//'+str(i)+'//'+'post.txt'
	
def split_post(basepath,filename,n,offset,debug=False):
	###############################################################################################
	#####################################################################
	# Loading the lines from the main post.txt file
	#####################################################################
	with open(filename,'r') as f:
		lines = f.readlines()
	lines = list(set(lines))
	#lines = lines[:50]'''-=-__=--=-__=--=-__=--=-__=--=-__=--=-__=--=-__=--=-__=--=-__=--=-__=--=-__=--=-__=--=-__=--=-__=-'''
	#print print_list(get_post_ids(lines),'\n================================\n')

	#####################################################################
	# Making sure they all have unique ids
	#####################################################################
	s = {}
	for line in lines:
		s[line.split('\t')[0]] = line
	print 'Lines  = '+str(len(lines))
	print 'Unique = '+str(len(s))
	lines = s.values()
	###############################################################################
	# Initializing the required parameters for the splitting process
	###############################################################################
	# Getting length of the list
	l = len(lines)
	########################
	''' FAKE DATA
	#l = 50
	#lines = range(l)
	#lines = [str(i) +'\n' for i in lines]
	'''
	#########################
	# Number of subsets to break it into
	# n = 10 ############### PASSED AS INPUT ARGUMENT
	# length of each subsegment
	m_float = l*1.0/n
	# Something goes wrong, then last one gets additional/less one or two posts for rounding
	print l,n,m_float
	############### Done with the core math Initialization

	###############################################################################
	# Initializing the parameters which will be needed in the process
	###############################################################################
	start = 0
	base_path = basepath+'//split_data'
	if not os.path.exists(base_path): os.makedirs(base_path)
	n_post_id = {}
	f_n_post_id = open(base_path+'//index.txt','w+')

	# If We already have a set of split folders, we want to create these folders 
	# at the end of them
	# so define offset
	# offset = 9041 ############### PASSED AS INPUT ARGUMENT
	# It will create folders from offset through (offset+n-1)
	# So the first folder will be offset
	###############################################################################
	#
	#                               THE PROCESS
	#
	###############################################################################
	print '===========================CREATING THE FOLDERS==========================='
	for i in range(offset,offset+n):
		
		# Now, creating a folder of name i
		new_path = base_path+'//'+str(i)
		if not os.path.exists(new_path): os.makedirs(new_path)
		
		# Getting slice boundaries from K-1 to K
		if start + m_float+ n >= l :  
			end = l
		else:
			end = start + int(m_float)
		
		#  Slicing it   
		sub_list = lines[start:end]
		
		# Converting it to a set, to remove all non-unique items
		sub_list = list(set(sub_list))
		
		# Creating a dictionary of the items in this folder
		n_post_id[i] = sub_list

		# Getting the list of post_ids
		sub_list_post_ids = get_post_ids(sub_list)

		# Writing this to the index file
		print 'Writing to index file'       
		for one_id in sub_list_post_ids   : 
			f_n_post_id.write(str(i)+'\t'+str(one_id)+'\n')
		
		
		# Now to write down the sliced contents to a new file
		#print 'Writing Contents to new file'
		with open(new_path+'//'+'post.txt','w+') as f:
			f.writelines(sub_list)
		
		print str(i)+' ' + 'Total : '+str(len(lines)),'This One :'+ str(len(sub_list)), 'Start : '+str(start),'End : '+str(end)
		start = end

	###############################################################################
	# Loading the stuff back from the different folders to see if stuff is fine
	###############################################################################
	if debug:
		print '===========================Loading the data back===========================' 
		post_dict = load_split_posts(base_path,n,offset)
		print 'Length of loaded data = '+str(len(post_dict))
	#print len(sub_list)
	#print list(sub_list)[0]
	#print get_post_ids(sub_list)

		