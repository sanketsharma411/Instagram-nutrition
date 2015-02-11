import pickle
################################################################################
# This file combines data from the clean_USDA_data.txt with the USDA_data_pickle file
# to create USDA_data_pickle_x file which has the updated/cleaned specs
# Use this when you get insecure string pickle error
# Requires
#   clean_USDA_data.txt  # to create id_spec_dict
#   USDA_data_pickle     # to combine it with the nut_info
# Creates
#   id_spec_dict
#   USDA_data_pickle_x
##################################################################################

# Reading the file
with open('clean_USDA_data.txt','r') as f:
    lines = f.readlines()
# Creating the id_spec_dict
id_spec_dict = {}
for line in lines:
    one_id,spec = line.split('\t')
    id_spec_dict[one_id] = spec

# Reading the nut_info from USDA_data_pickle
print 'Loading nut_info from USDA_data'
with  open('USDA_data_pickle','r') as f:
    USDA_main_dict = pickle.load(f)
print 'Done Loading'
