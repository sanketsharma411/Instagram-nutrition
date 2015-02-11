FOlder contains all the food lists, and related stuff


canonical_names_list.txt
	Contains the canonical names of food items
	To be used 
		a. in the 2-step comparison process
		b. as seed tags

=======================================RUN THIS BELOW FILE BEFORE THE MAIN FILE IN ROOT FOLDER====================================
combine_USDA_ids.py
	Reads the canonical names list file and attaches a USDA ID with it in the file can_form_USDA_id.txt
=======================================RUN THE ABOVE FILE BEFORE THE MAIN FILE IN ROOT FOLDER====================================
can_form_USDA_id.txt
	each line corresponds to one canonical name and its corresponding intersection with the USDA file
	i.e. can_name'\t'USDA_id_1','USDA_id_2....
	