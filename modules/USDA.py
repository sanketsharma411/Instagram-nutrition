import os, pickle,sys,inflect,numpy
    
this_dir,this_file = os.path.split(__file__)

p = inflect.engine()

############################################################################
#       Loading Nutrient data
############################################################################
# USDA : dict
# keys : USDA ids
# vals : dict 
#         'contents':nutrient description
#         'f_name' : something of historical importance, not needed now
#         'group'  : USDA grouping
#         'specs'  : descriptive tags of food item, same as in id_spec_dict
USDA_data_file = os.path.join(this_dir,'data','USDA','USDA_food_data.pickle')
with open(USDA_data_file,'r') as f:
    print 'Loading USDA data'
    USDA = pickle.load(f)

# nut_list : names of the nutrients we care about
nut_list = []
for nut_index in [3,30,21,18,14,23,25]:
    nut_list.append(USDA[USDA.keys()[0]]['contents'].keys()[nut_index])    

# id_spec_dict : dictionary
#   keys : USDA ids
#   vals : set of associated description from USDA    
id_spec_dict_file = os.path.join(this_dir,'data','USDA','id_spec_dict.pickle')
with open(id_spec_dict_file,'r') as f:
    print 'Loading id_specs'
    id_spec_dict = pickle.load(f)
    id_spec_dict = {id:set(specs.strip().split()) for id,specs in id_spec_dict.items()}    

# excluded_names : set of excluded_canonical names as describeed below
# excluded names i.e. which appear in food context by aren't indicative of nutritional values
excluded_names_file = os.path.join(this_dir,'data','canonical_names','excluded_names.txt')
with open(excluded_names_file,'r') as f:
    print 'Loading excluded canonical names'
    excluded_names = {x.strip() for x in f.readlines()}

###########################################################################
#  Pre-processing tags
###########################################################################
def pre_process_food_tag(tag):
    """ Pre-Process food tags before using them in nutrition computation 
    
    input  : single string 
    output : single string of the processed tag
    For invalid tags return empty string ''
    """    
    tag = tag.strip()
    singular_tag = p.singular_noun(tag) 
    # to avoid computing singluar_noun twice used if..else
    # 2x speed-up
    tag = singular_tag if singular_tag is not False else tag 
    return tag if tag not in excluded_names else ''
    
    
    
###############################################################################
#   Canonical Form Matching
###############################################################################
# Using the list of canonical names for matching tags to USDA ids

# can_name_id : dict
#   keys = canonical names
#   vals = USDA ids which include the name
canonical_names_USDA_file = os.path.join(this_dir,'data','canonical_names','canonical_names_USDA_id.txt')
with open(canonical_names_USDA_file,'r') as f:
    print 'Loading Canonical Food Names'
    lines = f.readlines()

can_name_id = {}
for line in lines:
    if len(line.split('\t')) > 1:
        can_name = line.strip().split('\t')[0]
        ids = [x for x in line.split('\t')[1].strip().split(',') if x != '']
        can_name_id[can_name] = ids

# Canonical_names is set of all canonical names to be used for checking containment
canonical_names = set(can_name_id.keys())
############################################################################
#       Mapping tags to USDA ids
############################################################################    
def tag2id(tags,**kwargs):
    '''Convert entered tags to matching USDA food ids with overlap length
    
    For any set of tags this function looks up the USDA food names and returns
    a length_match_dictionary [rename this function to reflect this change].
    which is a dictionary with keys as number of matching tags, and values as
    a dictionary with keys as the USDA ids and values as a list of matching tags
    present in that USDA_id

    Inputs:
        tags : A list of tags or string of comma/space separated tags		
        key-word arguments:
            canonical_match = Boolean
                if True:
                    USDA ids are found by first mapping tags to canonical_names
                    Then the canonical names to USDA
                else:
                    Default : Map tags directly to USDA

    Returns:
       ids  : list of matching USDA ids
       optionally : params
            A tuple of additional parameters obtained during matching
            params[0] = len_match_dict
                len_match_dict : {1:{id1:[],id2:[],id3:[]}, 2:{id4:[],id5:[]}}
                keys : length of overlap 
                vals : dict 
                        keys : USDA id 
                        vals : overlapping tags between entered tags and USDA entry 
        
    The idea is to use this function to get matching USDA entries with their details
    Then to obtain nutritional stats you can select all the ids or use the overlap
    lengths and implement something like a maximal matching
    '''
    
    if type(tags) == str :
        tags = tags.split(',') if ',' in tags else tags.split()
    
    # extracting from kwargs
    canonical_match = kwargs.get('canonical_match',False)
    id_params = kwargs.get('id_params',False)
    
    # Pre-processsing tags
    tags = [pre_process_food_tag(tag) for tag in tags if tag != '']
    
    # search_ids is basically our search space in USDA
    # by default we look at entire USDA for matching tags
    # if some other matchinng method is defined through kwargs
    # then use this to modify the search space as needed
    search_ids = id_spec_dict.keys()
    
    
    # if canonical match is true, we go with 2-step matching 
    # first map tags to canonical names
    # then canonical names to USDA ids
    if canonical_match:
        # We thus do not have to search through entire USDA but only through 
        # items which have have canonical_names present in them
        can_match_ids = (can_name_id[tag] for tag in tags if tag in canonical_names)
        can_match_ids = [can_match_id for one_match in can_match_ids for can_match_id in one_match]        
        search_ids = can_match_ids

    # Looking up the USDA data
    len_match_dict = {}
    for spec_id in search_ids:
    
        # Gathering matching USDA ids
        matches = [tag for tag in tags if tag in id_spec_dict[spec_id]]
        
        if len(matches) == 0:
            # If no matches found move on to the next USDA item
            continue
        
        # Putting in the len_match_dict
        len_match_dict.setdefault(len(matches),{})[spec_id] = matches
        
    match_ids = [key for length in len_match_dict.keys() for key in len_match_dict[length].keys()] 
    
    # Combining the additional parameters int one params variable
    params = [len_match_dict]
    
    
    return match_ids,params

############################################################################
#       Selecting the best USDA matching tags for this one
#         based on whatever selection criteria you want
############################################################################    
def select_ids(id_params, **kwargs):
    '''Select representative USDA ids based on len_match_dict
    
    The representative USDA ids for the given set of tags can be selected in 
    various ways (maximal-matching, backoff model,etc..) The selection is 
    implemented here. Use kwargs to pass relevant parameters for the selection 
    method. 

    The default matching is to select all the ids

    input : 
    
        ids_params is the tuple obtained from tag2id
        
        keyword-arguments:
        	maximal_len : Boolean
        		True => Select USDA ids based on maximal length matching
        		else => Default matching

    output: list of ids
    '''
    
    if len(id_params) == 1:
        # We only have ids, and thus no way to prioritize any of them
        return id_params[0]
        
    ids = id_params[0]
    match_dict = id_params[1][0]
    
    # Extracting from kwargs
    maximal_len = kwargs.get('maximal_len',False)
    
    
    # Validating input
    if match_dict == -1 or not match_dict:
        return [-1]
    
    # Initializing
    match_ids = []
    
    
    if maximal_len:
        # If maximal matching is true, then do select the ids which have a maximal matching length
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
#   Computing nutrient values from selected ids
###############################################################################
def id2nut(USDA_ids):
    '''Compute nutrient values from matching USDA ids
    
    Input : List/iterable of USDA ids
    Output: Dictionary with keys = nutrient names, values = corresponding values (numpy.int)

    Math : 
        for each nutrient nut:
            mean = mean(nut for all USDA matches)
	    std  = standard_deviation(nut for all USDA matches)
	    if std > mean => result = max (nut for all USDA matches)
	    else => result = mean

    Use kwargs later to select other computation methods if needed
    '''
    # Validating
    if USDA_ids == [-1] or not USDA_ids :
        return [-1]
    

    # Gathering values from USDA database
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
    
