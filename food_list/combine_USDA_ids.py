import sys
sys.path.append('C:\Users\Shweta\Desktop\CS 8903\FINAL\scripts')
import os
os.chdir('C:\Users\Shweta\Desktop\CS 8903\FINAL')
import inflect
p = inflect.engine()
################################################################################
########## Because it has to use stuff from Instalib, analyze_utils ############
########## and match_utils, we have changed the directory as above  ############
################################################################################
from InstaLib import *
from analyze_utils import *
from match_utils import *
################################################################################
#       Reading the main file
################################################################################
with open('food_list\\canonical_names_list_updated.txt','r') as f:
    lines = f.readlines()
################################################################################
#       Converting it to Lower case + Singular
################################################################################
with open('food_list\\canonical_names_list_updated_lower_singular.txt','w+') as f:
    for line in lines:
        word = line.strip().lower()
        word = p.singular_noun(word) if p.singular_noun(word) else word
        f.write(word+'\n')
################################################################################
#       Reading the same file created above
################################################################################
with open('food_list\\canonical_names_list_updated_lower_singular.txt','r') as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]    
################################################################################
#       Attaching USDA ids to the file
################################################################################
match_len = []
with open ('food_list\\can_form_USDA_id.txt','w+') as f:
    for line in lines:
        len_dict = tag2id(line)
        if bool(len_dict):
            matched_ids = len_dict[1].keys() 
        else:
            matched_ids = []
        match_len.append(len(matched_ids))
        line += '\t'+print_list(matched_ids,',')+'\n'
        print line
        f.write(line)
    