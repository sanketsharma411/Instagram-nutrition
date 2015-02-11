import sys,inflect
sys.path.append('C:\Users\Shweta\Desktop\CS 8903\FINAL\scripts')
#sys.path.append('/nethome/ssharma321/FINAL/scripts')
from InstaLib import *
import pickle, numpy, os
from collections import defaultdict
os.chdir('C:\Users\Shweta\Desktop\CS 8903\\FINAL')
#os.chdir('/nethome/ssharma321/FINAL/')
p = inflect.engine()
############################################################################
#       Loading the USDA data
############################################################################
with open('USDA/id_spec_dict','r') as f:
    id_spec_dict = pickle.load(f)

all_specs_list = []
# Modifying it to a set
for k in id_spec_dict.keys():
    # Creating a list of all the specs, so that the random tags are not looked up
    # in the 8618 items
    all_specs_list.extend(id_spec_dict[k].split())
    id_spec_dict[k] = set(id_spec_dict[k].split())
all_specs_set = set(all_specs_list)
############################################################################
#       Loading the negative words data
############################################################################    
with open('food_list/neg_words.txt','r') as f:
    lines = f.readlines()
neg_words = set([line.strip() for line in lines])
############################################################################
#       Mapping tags to all the matching tags in USDA
############################################################################    
def tag2id(tags):
    '''
    tags can be either a list or string of tags separated by commas or spaces
    Implement the matching function here
    Matches the stuff in the USDA database to the stuff in the tags and returns a 
     match length sorted dictionary of matches and ids and
    input : tags : string
    output: len_match_dict = {1:{id:[],id:[],id:[]}, 2:{id:[],id:[]}}
    output: neg_matches = ['list','of','words','which','match','the','neg','words']
    The idea is to do the matching once, and then we use multiple welection functions 
    to select what to set as the id and what to not
    '''     
    if type(tags) == str :
        tags = tags.split(',') if ',' in tags else tags.split()
    len_match_dict = {}
    # Cleaning up the tags
    tags_new = []
    for tag in tags:
        ################## Pre-processing here ###############################
        tag = tag.strip()
        tag = p.singular_noun(tag) if p.singular_noun(tag) else tag
        ######################################################################
	tags_new.append(tag)
    for spec_id in id_spec_dict:
        matches = []
        for tag in tags:
            if tag in id_spec_dict[spec_id]: #[ .split() done to make sure that food does not match fastfood]
                matches.append(tag)
        if len(matches) == 0:
            continue
        if len(matches) not in len_match_dict:
            len_match_dict[len(matches)] = {}
        len_match_dict[len(matches)][spec_id] = matches
        
    # Now for the bad matches
    #### EDIT 22 DECEMBER 
    # Removed the negative matches i.e. the next line
    # neg_matches = [word for word in neg_words if word in tags]
    return len_match_dict #, neg_matches
	
def tag2id_dabba(tags):
    '''
    tags can be either a list or string of tags separated by commas or spaces
    Implement the matching function here
    Matches the stuff in the USDA database to the stuff in the tags and returns a 
     match length sorted dictionary of matches and ids and
    input : tags : string
    output: len_match_dict = {1:{id:[],id:[],id:[]}, 2:{id:[],id:[]}}
    output: neg_matches = ['list','of','words','which','match','the','neg','words']
    The idea is to do the matching once, and then we use multiple welection functions 
    to select what to set as the id and what to not
    '''     
    if type(tags) == str :
        tags = tags.split(',') if ',' in tags else tags.split()
    len_match_dict = {}
    for spec_id in id_spec_dict:
        matches = []
        for tag in tags:
            ################## Pre-processing here ###############################
            tag = tag.strip()
            tag = p.singular_noun(tag) if p.singular_noun(tag) else tag
            ######################################################################
            if tag in id_spec_dict[spec_id].split(): #[ .split() done to make sure that food does not match fastfood]
                matches.append(tag)
        if len(matches) == 0:
            continue
        if len(matches) not in len_match_dict:
            len_match_dict[len(matches)] = {}
        len_match_dict[len(matches)][spec_id] = matches
        
    # Now for the bad matches
    #### EDIT 22 DECEMBER 
    # Removed the negative matches i.e. the next line
    # neg_matches = [word for word in neg_words if word in tags]
    return len_match_dict #, neg_matches

############################################################################
#       Selecting the best USDA matching tags for this one
# based on whatever selection criteria you want
############################################################################    
def select_ids(match_dict, maximal_length_matching = False):
    '''
    Here is passed the match_dict and we return a list of ids 
    Implement the id selection function here
    '''
    if match_dict == -1 or not match_dict:
        return [-1]
    match_ids = []
    
    if maximal_length_matching:
        # If maximal matching is true, then do the following
        if len(match_dict[match_dict.keys()[-1]]) == 1:    # The largest has just one match, so go one step back
            match_ids.append(match_dict[match_dict.keys()[-1]].keys()[0])# Note this one
            if len(match_dict) > 1:                         
                # If length is more than one, then pick up the one before it as well
                match_ids.extend(match_dict[match_dict.keys()[-2]].keys())
                #for spec_id in match_dict[match_dict.keys()[-2]].keys():
                #    match_ids.append(spec_id)
        else:
            match_ids.extend(match_dict[match_dict.keys()[-1]].keys())
            #for spec_id in match_ids.extend(match_dict[match_dict.keys()[-1]].keys()):
            #        match_ids.append(spec_id)
        # Else just return all the usda matched ids
    else:
        for key in match_dict.keys():
            id_count_dict = match_dict[key]
            match_ids.extend(id_count_dict.keys()) 
        
        
    return match_ids        
        
###############################################################################
#   Loading USDA data and setting the required stuff up
###############################################################################
with open('USDA/USDA_data_pickle_x','r') as f:
    print "Loading USDA data"
    USDA = pickle.load(f)
nut_list = []
for nut_index in [3,30,21,18,14,23,25]:
    nut_list.append(USDA[USDA.keys()[0]]['contents'].keys()[nut_index])    

###############################################################################
#   Modifying it to work with only post_ids
###############################################################################
def id2nut(USDA_ids):
    '''
    
    Returns the nutritional values of the 5 nutrients, based on the 
    passed list of USDA_ids. It uses the mean>std and stuff to compute the
    nutritional values
    The returned values are numpy type, so be careful with their precision
		while printing 
    '''
    if USDA_ids == [-1] or not USDA_ids :
        return -1
    if type(USDA_ids) == str and ',' in USDA_ids:
        USDA_ids = USDA_ids.split(',')
    temp_nut_val_dict = dict.fromkeys(nut_list)
    for nut in nut_list:                                    # Empty list to store the nutritional information,
        temp_nut_val_dict[nut] = list()                     # of each food_id
    for food_id in USDA_ids:                                    # for each food id                               
        # Populate the temp_nut_val_dict defined above
        for nut in nut_list:                            # for each nutrient append its value to the list
            temp_nut_val_dict[nut].append(float(USDA[food_id]['contents'][nut]))


    # The Math
    final_nut_dict = dict.fromkeys(nut_list)                # this dict holds the final value of the nutritional info for each post
    for nut in temp_nut_val_dict:                           # For each nutrient in the dict
        l = temp_nut_val_dict[nut]                          #   list of the values
        if numpy.std(l) > numpy.mean(l):                    #   if the standdard deviation is more than the mean
            final_nut_dict[nut] = numpy.max(l)              #       then the value is the max
        else:                                               #   else 
            final_nut_dict[nut] = numpy.mean(l)             #       it is the mean

    return final_nut_dict
###############################################################################
#   Canonical Form Matching
###############################################################################
#with open('/nethome/ssharma321/FINAL//food_list//can_form_USDA_id.txt','r') as f:
#    lines = f.readlines()
lines = read_lines('food_list\\can_form_USDA_id.txt')
can_form_id_dict = {}
for line in lines:
    if len(line.split('\t')) > 1:
        can_form = line.strip().split('\t')[0]
        ids = line.split('\t')[1].strip().split(',')
        can_form_id_dict[can_form] = ids
# improving it
for can_form in can_form_id_dict:
    if can_form_id_dict[can_form] == ['']:
        can_form_id_dict[can_form] =[]
canonical_name_set = set(can_form_id_dict.keys())
###############################################################################
def in_can_list(tag):
    '''
    Give a tag, and I will tell you if it is in the canonical forms list or not
    '''
    return tag in canonical_name_set
        
###############################################################################
def tag2id_can_match(tags):
    '''
    tags can be either a list or string of tags separated by commas or spaces
    For a list of input tags, this function does the 2-Step matching with the
    stuff present in the file food_list\\can_form_USDA_id.txt, and returns
    a list of ids from the USDA database which match the entered USDA tags
    Depends on food_list\\can_form_USDA_id.txt
        make changes to the file canonical_names_list.txt
        And the file combine_USDA_ids.py in the food_list folder
    The work of getting the info is done right above this function
    '''
    if type(tags) == str :
        tags = tags.split(',') if ',' in tags else tags.split()
    id_list = []
    tag_list = []
    for tag in tags:
        ################## Pre-processing here ###############################
        tag = tag.strip()
        tag = p.singular_noun(tag) if p.singular_noun(tag) else tag
        ######################################################################
        if  tag in  canonical_name_set:
            id_list.extend(can_form_id_dict[tag])
            tag_list.append(tag)
    return list(set(tag_list)),list(set(id_list ))
    
###############################################################################
#  Now searching only in the usda items which match the canonical forms
###############################################################################
def len_match_2_step(tags,ids):
    '''
    Does the length match for only the ids passed here
    i.e. doing the searching in only the 
    '''
    new_dict = {k:id_spec_dict[k] for k in id_spec_dict.keys() if k in ids}
    len_match_dict = {}
    tags = tags.split(',')
    for spec_id in new_dict:
        matches = []
        for tag in tags:
            ################## Pre-processing here ###############################
            tag = tag.strip()
            tag = p.singular_noun(tag) if p.singular_noun(tag) else tag
            ######################################################################
            if tag in new_dict[spec_id].split():
                matches.append(tag)
        if len(matches) == 0:
            continue
        if len(matches) not in len_match_dict:
            len_match_dict[len(matches)] = {}
        len_match_dict[len(matches)][spec_id] = matches
    return len_match_dict
###############################################################################
#   The old function
###############################################################################

def post_to_nut_old(tags):
    boolean = False
    tags = tags.lower()
    st = tags + '\t'
    food_id_count = defaultdict(int)
    ######
    # Dictionary of type
    #   {   nutrient_1 :[val_descid_1, val_descid_2, val_descid_3,...]
    #       nutrient_2 :[val_descid_1, val_descid_2, val_descid_3,...]
    #   }
    #   Then we compute the mean and variance for each nutrient from this list
    #
    temp_nut_val_dict = dict.fromkeys(nut_list)
    for nut in nut_list:                                    # Empty list to store the nutritional information,
        temp_nut_val_dict[nut] = list()                     # of each food_id
    ##############################
    for food_id in USDA:                                    # for each food id 
        matched_specs = []                                  # Empty list to hold the matched food ids
        for spec in USDA[food_id]['specs'].split(' '):      # for each specification for this id
            # Insert Similarity function here
            if spec != '' and spec in tags:                 # if the specification is not blank and is in the taglist
                food_id_count[food_id] += 1                 # increment the score of this food_id, done for seeing at the end which one has the highest matches and such stuff
            # Insert Similarity function here
                matched_specs.append(spec)                  # Append this id to the empty list
                
        if food_id_count[food_id] > 2:                      # Now if for this food  the number of matches is >2 Threshold
            temp_nut_dict = {}                              
            st += str(food_id) + ':' + str(matched_specs) +','

            # Populate the temp_nut_val_dict defined above
            for nut in nut_list:                            # for each nutrient append its value to the list
                temp_nut_val_dict[nut].append(float(USDA[food_id]['contents'][nut]))
            boolean = True                                  # To mark that there is a match for this post in the USDA DB

    #### Now do the computation for each list
    if boolean == False:
        return -1

    # The Math
    final_nut_dict = dict.fromkeys(nut_list)                # this dict holds the final value of the nutritional info for each post
    for nut in temp_nut_val_dict:                           # For each nutrient in the dict
        l = temp_nut_val_dict[nut]                          #   list of the values
        if numpy.std(l) > numpy.mean(l):                    #   if the standdard deviation is more than the mean
            final_nut_dict[nut] = numpy.max(l)              #       then the value is the max
        else:                                               #   else 
            final_nut_dict[nut] = numpy.mean(l)             #       it is the mean

    return final_nut_dict

###############################################################################
#   Now writing these selected ids to a file
def  print_nut_info_in_order(nut_info):
    # energy TAB sugar TAB fat TAB cholesterol TAB fiber TAB protein
    if nut_info == -1:
        return '-1\t-1\t-1\t-1\t-1\t-1'
    st = ''
    st += '%0.3f' %(nut_info[('Energy', 'kcal')])+'\t'
    st += '%0.3f' %(nut_info [   ('Sugars, total', 'g')])+'\t'
    st += '%0.3f' %(nut_info  [  ('Total lipid (fat)', 'g')])+'\t'
    st += '%0.3f' %(nut_info   [ ('Cholesterol', 'mg')])+'\t'
    st += '%0.3f' %(nut_info    [('Fiber, total dietary', 'g')])+'\t'
    st += '%0.3f' %(nut_info    [('Protein', 'g')])
    return st

##################################################################################
#    Printing the nut_info_lists obtained by vanilla 2 step and by maximal 2 step
##################################################################################
    
def print_2_nut_info_in_order(nut_info_1, nut_info_2):
    st = ''
    st += '%0.3f' %(nut_info_1[('Energy', 'kcal')])+' | '
    st += '%0.3f' %(nut_info_2[('Energy', 'kcal')])+'\t'
    st += '%0.3f' %(nut_info_1[('Sugars, total', 'g')])+' | '
    st += '%0.3f' %(nut_info_2[('Sugars, total', 'g')])+'\t'
    st += '%0.3f' %(nut_info_1[('Total lipid (fat)', 'g')])+' | '
    st += '%0.3f' %(nut_info_2[('Total lipid (fat)', 'g')])+'\t'
    st += '%0.3f' %(nut_info_1[('Cholesterol', 'mg')])+' | '
    st += '%0.3f' %(nut_info_2[ ('Cholesterol', 'mg')])+'\t'
    st += '%0.3f' %(nut_info_1[('Fiber, total dietary', 'g')])+' | '
    st += '%0.3f' %(nut_info_2[('Fiber, total dietary', 'g')])+'\t'
    st += '%0.3f' %(nut_info_1[('Protein', 'g')])+' | '
    st += '%0.3f' %(nut_info_2[('Protein', 'g')])
    return st

##################################################################################
#    Print nut_info_nicely
##################################################################################

def  print_nut_info_nicely(nut_info):
    # energy TAB sugar TAB fat TAB cholesterol TAB fiber TAB protein
    if nut_info == -1:
        return '-1\t-1\t-1\t-1\t-1\t-1'
    st = ''
    st += '     Energy : ' + '%0.3f' %(nut_info[('Energy', 'kcal')])+'\n'
    st += '    Protein : ' +'%0.3f' %(nut_info [   ('Sugars, total', 'g')])+'\n'
    st += '  Lipid Fat : ' +'%0.3f' %(nut_info  [  ('Total lipid (fat)', 'g')])+'\n'
    st += 'Cholesterol : ' +'%0.3f' %(nut_info   [ ('Cholesterol', 'mg')])+'\n'
    st += '      Fiber : ' +'%0.3f' %(nut_info    [('Fiber, total dietary', 'g')])+'\n'
    st += '    Protein : ' +'%0.3f' %(nut_info    [('Protein', 'g')])
    return st
