import urllib, HTMLParser, urllib2, inflect
import sys, random, pickle, numpy, os
import pprint as pp
from bs4 import BeautifulSoup
from collections import defaultdict
from InstaLib import *
########################################################################
#   Importing stuff for setting the local time
########################################################################
import datetime, pytz
from tzwhere import tzwhere 
w = tzwhere.tzwhere()
########################################################################
#
# Post to nut
# This file maps each post id to a nutritional value
#
########################################################################
os.chdir('C:\Users\Shweta\Desktop\CS 8903\FINAL')
#os.chdir('/nethome/ssharma321/FINAL/')
################################################################################################
# Getting the required stuff
################################################################################################
with open('USDA/USDA_data_pickle_x','r') as f:
    print "Loading USDA data"
    USDA = pickle.load(f)
################################################################################################
# Setting up the list of our interest's nutrients
# [3-Sodium, 30-Energy, 21-Protein, 18-Cholestrol, 14-Fiber, 23-Sugars, 25-Total Lipid ]
# Had a look at the data to figure out these values, It might help looking at the data again and
# changing these
################################################################################################
nut_list = []
for nut_index in [3,30,21,18,14,23,25]:
    nut_list.append(USDA[USDA.keys()[0]]['contents'].keys()[nut_index])
    
################################################################################################
#                     Loading the data
################################################################################################
def load_post(file_name, set_loc_time = False):
    count = 0
    print 'Loading the post File'
    with open( file_name,'r') as f:
        lines = f.readlines()
    
    print 'Loading the post File !! DONE !!'
    print 'Reading through the loaded data into local variables'
    post_dict = {}
    for line in lines:
        inst = line.split('\t')
        if len(inst) != 16:            # If this is not a good line in the file
            continue
        post_id = inst[0]
        try:
            post_dict[post_id] = Post(inst)     # SKIP
        except:
        #    continue
            count += 1
    print 'Reading through the loaded data into local variables !! DONE !!', count
    '''
    print 'Setting the local time info'
    loc_count = 0
    for post_id in post_dict:
        if post_dict[post_id].loc:
            post_dict[post_id].set_loc_time()
            loc_count += 1
        else:
            post_dict[post_id].has_loc_time = False
    print 'Setting the local time info !! DONE !!',loc_count
    '''
    return post_dict
################################################################################################
#                     Defining the class
################################################################################################
class Post:
    # Declare global variables here

    # Now on to the first constructor
    def __init__(self, inst):
        self.id = inst[0]
        self.time = float(inst[4])
        self.url = inst[5]
        self.seed_tag = inst[7] 
        self.tags = inst[8]#.split(',')
        self.caption = inst[11] if inst[11] != 'NA' else '' 
        self.likes = int(inst[14])
        self.is_image = (inst[2] == 'image')
        self.media_url = inst[9]
        self.has_nuts = False
        self.calories = -1
        self.comments = {}
        self.comm_text = ''
        self.num_comments = int(inst[13]) if inst[13] != '' else 0
        self.num_tot_comments = 0
        if inst[12].split(',')[0] != 'NA':
            if inst[12].split(',') < 4:
                print len(inst[12].split(',') )
            self.loc_info = inst[12].split(',')
            self.has_loc = True
            self.lat = float(self.loc_info[0])
            self.lon = float(self.loc_info[1])
            self.loc_id = self.loc_info[-1]
            self.loc_name = ' '.join(self.loc_info[2:-1])
        else:
            self.has_loc = False

    
    # To String function
    def __str__(self):
        st = self.id+'\n'
        st += 'Created on   = '+ str(self.time) + '\n'
        st += 'Tags         = ' + self.tags+ '\n'
        st += 'Caption      = ' + self.caption+ '\n'
        st += 'Nutritional  = ' + str(self.has_nuts)+'\n'
        st += 'Calories     = '+ str(self.calories)+'\n'
        st += 'Num Likes    = ' + str(self.likes) + '\n'
        st += 'Num Comments = ' + str(self.get_num_comments()) + '\n'
        #st += 'Comments     = ' + self.comm_text + '\n'
        
        return st

    # setting the nutrition info
    def set_nut_info(self,line):
        #print nut_info
        line = line.strip().split('\t')
        self.check_tags = line[1].strip('"')
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

    def set_cal_class(self, boolean):
        self.high_cal = boolean

    def get_nut_info(self):
        if self.has_nuts :
            st =  '       Tags : ' +print_list(self.tags,',')+'\n'
            st += 'Word Matches: ' +print_list(self.match_words,',')+'\n'
            st += ' ID Matches : ' +print_list(self.match_ids,',')+'\n'             
            st += '     Energy : ' +self.calories+'\n'
            st += '    Protein : ' +self.sugar+'\n'
            st += '  Lipid Fat : ' +self.fat+'\n'
            st += 'Cholesterol : ' +self.cholesterol+'\n'
            st += '      Fiber : ' +self.fiber+'\n'
            st += '    Protein : ' +self.protein+'\n'
            return st
        else:
            return 'Sorry, the tags : '+self.tags+' matched nothing'
    
    def set_loc_time(self):
        '''
        Given the UTC time, latitude and longitude, This converts the passed time into
        local time, using the lat, lon info passed
        All are expeccted to be floats
        '''
        if self.has_loc == 0:
            self.has_loc_time = False
            return None
        lat = self.lat
        lon = self.lon
        
        # Getting the local timezone Name
        self.local_tz_name = w.tzNameAt(lat,lon)
        if self.local_tz_name == None:
            self.has_loc_time = False
            return None
        UTC_time = float(self.time)
        # Converting back from the timestamp
        dt = datetime.datetime.utcfromtimestamp(UTC_time)
        # Saving the original unlocalized time
        dt_og = dt
        # Localizing the time, i.e. attaching the UTC information
        dt = pytz.utc.localize(dt)
        # Getting the local timezone
        local_tz = pytz.timezone(self.local_tz_name)
        # Getting the offset from UTC to this timezone
        offset = dt.astimezone(local_tz).utcoffset()
        # Adding the offset to the original time to get the new localized time
        # Need to subtract one hour from this time because it is off by one hour, i.e.
        # It adds an extra hour
        self.loc_time = dt_og+offset
        self.has_loc_time = True

    
    # setting the comments
    def set_comment(self,line):
        line = line.strip().split('\t')
        if len(line) == 5 and not line[1] in self.comments :
            self.comments[line[1]] = Comment(line)
            self.comm_text += self.comments[line[1]].text+'\n'
            self.num_tot_comments += 1

    #def get_num_comments(self):
    #	return self.num_tot_comments if self.num_tot_comments > self.num_comments else self.num_comments
    def get_num_comments(self):
        num_comment = int(str(self.num_comments) + '0')
        if num_comment == 0:
            return self.num_tot_comments
        else:
            return max(num_comment, self.num_tot_comments)
            
class Comment:
    def __init__(self, line):
        #line = line.strip().split('\t')
        self.comm_id = line[1]
        self.time = line[2]
        self.text = line[3]
        self.user_id = line[4]

    def __str__(self):
        st = self.text+'\n'
        st+= self.time+'\t'+self.user_id
        return st
    
###############################################################################
#       Getting those USDA ids which have a given word
###############################################################################
p = inflect.engine()
def get_USDA_ids(tag):
    l = []
    tag = tag.strip()
    tag = p.singular_noun(tag) if p.singular_noun(tag) else tag
    for k in USDA:
        if tag in USDA[k]['specs'].split():
            l.append(k)
    return l
###############################################################################
#    Getting the entries which co-occur with the given USDA entry    
###############################################################################
def get_rel_tags(tag):
    k = []
    tag = tag.strip()
    tag = p.singular_noun(tag) if p.singular_noun(tag) else tag
    for USDA_id in get_USDA_ids(tag):
        k.extend(USDA[USDA_id]['specs'].split())
    return k
###############################################################################
#    Getting the matching tags from the len_match_dict
###############################################################################
## Note function not extendable to include maximal matching
def print_match_tags(len_match_dict):
    matches = []
    for length in len_match_dict.keys():
        d = len_match_dict[length]
        for usda_id in d.keys():
            matches.extend(d[usda_id])
    return list(set(matches))

##########################################################################...#####
#    Getting the matching ids from the len_match_dict
###############################################################################
## Note function not extendable to include maximal matching
def print_match_ids(len_match_dict):
    matches = []
    for length in len_match_dict.keys():
        d = len_match_dict[length]
        matches.extend(d.keys())
    return list(set(matches))










