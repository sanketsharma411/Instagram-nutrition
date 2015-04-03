print 'Ganpati Bappa Moriya'
import sys, urllib
sys.path.append('/nethome/ssharma321/FINAL/scripts')
#sys.path.append('C:/Users/Shweta/Desktop/CS 8903/FINAL/scripts')
from InstaLib import *
from analyze_utils import *
from match_utils import *
from random import shuffle, randint
from datetime import datetime
import numpy as np
##########################################################################################
# Defining the Function to do the conversion of tags to nutritional infoinformation
##########################################################################################
def tag2nuts(tags):
    
    print '======================================================================================'
    st = str(tags)+ '\t'
    
    tag_list,id_list = tag2id_can_match(tags)
    
    if id_list: # Agar match mila
        print 'CANONICAL MATCH HUA'
        
        nut_info = id2nut(id_list)
        
        st += print_list(tag_list,';')+'\t'
        st += print_list(id_list,';') +'\t'
        st += print_nut_info_in_order(nut_info) +'\t'
        st += '1' +'\n'
        
        return st,1
    
    else:       # Agar can match nahi mila
        len_match_dict = tag2id(tags)
        
        if len_match_dict:
            
            print 'GHANTA MATCH HUA'
            
            tag_list = print_match_tags(len_match_dict)
            id_list = select_ids(len_match_dict,True)
            nut_info = id2nut(id_list)
            
            st += print_list(tag_list,';')+'\t'
            st += print_list(id_list,';')+'\t'
            st += print_nut_info_in_order(nut_info)+'\t'
            st += '0' +'\n'
            return st,2
    
        else:
            
            return st+'-1\n',3    

##########################################################################################
#    Defining the Paths   
##########################################################################################
# this path contains the split_data folder which contains the numbered folders
#main_path = 'C:/Users/Shweta/Desktop/CS 8903/FINAL/for_server/'
main_path = '/nethome/ssharma321/split_data/3/'
##############################################################################################
################################ THIS CHANGES FROM FILE TO FILE ##############################
i = 0
################################ THIS CHANGES FROM FILE TO FILE ##############################
##############################################################################################
base_path = main_path + '//'+str(i)
filename = base_path+'//post.txt'
#filename = '/nethome/ssharma321/sample_post.txt'
#filename = '/nethome/ssharma321/clean_post.txtclean.txt'
#filename = '/nethome/ssharma321/clean_post.txtclean2.txt'
print filename

##############################################################################################
#   Loading the file in 
##############################################################################################
with open(filename,'r') as f:
    lines = f.readlines()

#######################################################################
#   Loading the incomplete file in
#######################################################################
done_post_id_set = set()
try:
    with open(filename+'.nut','r') as f:
        old_nut_lines = f.readlines()
    
    print len(lines)
    # Getting the post_ids
    for line in old_nut_lines:
        done_post_id_set.add(line.split('\t')[0])
    print len(done_post_id_set)
except:
    pass
# Now making a pass through all the lines and
# removing the lines which have their post_id already in the above set
# Not making any changes to the main for loop down, so that each one
# need not be compared with stuff in the list, will have to make 2 passes
# through the data, but okay, we are cool with that coz each file is around 300MB
# and we aren't short on time, are we ?
cleaned_lines = []
for line in lines:
    if not line.split('\t')[0] in done_post_id_set:
        cleaned_lines.append(line)
lines = set(cleaned_lines)
print len(lines)

# Writing the status in the status file
with open(base_path+'//post_2_nut_interim_status.txt','a+') as f_status:
    f_status.write('!!!!!!!! Resuming Stuff !!!!!!'+'\n')
    f_status.write(str(datetime.now())+'\t')
    f_status.write('Already Completed = '+str(len(done_post_id_set))+'\tLeft = '+str(len(lines))+'\n')

#######################################################################
#   Back to the regular work, i.e. resuming
#######################################################################
count = 0
count_clean_hit = 0
count_nope_hit = 0
count_miss = 0

with open(filename+'.nut','a+') as f:
    for line in lines:  
        count += 1
        line = line.split('\t')
        st = line[0]+'\t'
        tags = line[8]
        nut_info,status = tag2nuts(tags)
        #nut_info,status = (1,1)
    
        if status == 1:
            count_clean_hit += 1
        elif status == 2:
            count_nope_hit += 1
        else:
            count_miss += 1     
    
        st += nut_info

        print st
        f.write(st)

        if not count%100:
            #with open('/nethome/ssharma321/post_2_nut_interim_status.txt','a+') as f_status:
            with open(base_path+'//post_2_nut_interim_status.txt','a+') as f_status:
                f_status.write(str(datetime.now())+'\t')
                f_status.write('Count = '+str(count)+'\tClean = '+str(count_clean_hit)+'\tNope = '+str(count_nope_hit)+'\tMiss = '+str(count_miss)+'\n')

with open(base_path+'//post_2_nut_interim_status.txt','a+') as f_status:
    f_status.write('!!!!!!!! WORK DONE !!!!!!'+'\n')
    f_status.write(str(datetime.now())+'\t')
    f_status.write('Already Done = '+str(len(done_post_id_set))+'\tCount = '+str(count)+'\tClean = '+str(count_clean_hit)+'\tNope = '+str(count_nope_hit)+'\tMiss = '+str(count_miss)+'\n')
