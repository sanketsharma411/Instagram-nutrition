
# coding: utf-8

# In[1]:

import sys
sys.path.append('../../food_deserts')
from M16 import *
from tract_utils import *


# ### Loading the data in M16 format

# In[2]:

with open('post.txt.nut.US','r') as f:
    lines = f.readlines()
lines = [line.strip().split('\t') for line in lines if len(line)>10]


# ### Generating tract_post_dict

# In[3]:

tract_post = {}
for line in lines:
    tract = line[-2][:11]
    if tract not in tract_post:
        tract_post[tract] = []
    tract_post[tract].append(line)


# ### Central to our work would be the tract_dict
# Where key is a tract and value a dict of the following parameters of the tract
# - fd : is this Food desert, 1 => Food Desert 
# - avg_cal : Average Calories 
# - avg_sug : Sugar
# - avg_fat :  " "
# - avg_cho :  " "
# - avg_fib :  " "
# - avg_pro :  " "
# - num_posts : Number of posts we have seen, i.e. length of the list for this tract in tract_post_dict
# - avg_posts : Average Post per day [I am not very sure as to how is this to be calculated]
# - centroid : (lat,long)
# - State : 2 digit state postal code, to be used to identify region
# - POP2010 : Population in 2010
# - LowIncomeTracts : '1' => Low Income
# - Rural : '1' => Rural
# - UATYP10 : 'C' or 'R' or 'U' dunno what they mean
# - topic model distribution

# #### Initializing the tract dict

# In[4]:

tract_dict = {}
for tract in tract_post:
    if tract not in tract_dict:
        tract_dict[tract] = {}


# ### Food Desert

# In[5]:

for tract in tract_post:
    fd = isFD(tract)
    tract_dict[tract]['fd'] = '1' if fd else '0'


# ### Average Nutrients

# In[6]:

for tract in tract_post:
    avg_nut = avgNuts(tract_post[tract])
    tract_dict[tract]['avg_cal'] = avg_nut[0]
    tract_dict[tract]['avg_sug'] = avg_nut[1]
    tract_dict[tract]['avg_fat'] = avg_nut[2]
    tract_dict[tract]['avg_cho'] = avg_nut[3]
    tract_dict[tract]['avg_fib'] = avg_nut[4]
    tract_dict[tract]['avg_pro'] = avg_nut[5]


# ### Total Number of Posts

# In[7]:

for tract in tract_post:
    tract_dict[tract]['num_posts'] = len(tract_post[tract])


# ### Average Post per day [kaise?]

# In[8]:

for tract in tract_post:
    tract_dict[tract]['avg_posts'] = avgPostsPerDay(tract_post[tract])


# ### Centroid

# In[9]:

for tract in tract_post:
    tract_dict[tract]['centroid'] = getCentroid(tract_post[tract])


# ### Socio-Economic Numbers

# #### Loading Tract Info

# In[11]:

tract_info = getTractInfo('../../food_deserts/data/tract_info.csv')


# #### Selecting tract parameters

# In[12]:

tract_params = ['State','POP2010','LowIncomeTracts','Rural','UATYP10']


# #### Joining the tract info to the tract_dict

# In[14]:

tracts_no_info = set()
for tract in tract_dict:
    if tract in tract_info:
        info_params = dict.fromkeys(tract_params)
        for param in tract_params:
            info_params[param] = tract_info[tract][param]
        tract_dict[tract].update(info_params)
    else:
        tracts_no_info.add(tract)

print len(tracts_no_info)

with open('missing_tracts','w+') as f:
    for tract in tracts_no_info:
        f.write(tract2line(tract,tract_dict[tract], missing = True)+'\n')


# #### For stuff which does not have socio econimic numbers, we skip them

# In[15]:

for tract in tracts_no_info:
    del tract_dict[tract]


# #### Writing to file

# In[16]:

with open('tracts.tsv','w+') as f:
    for tract in tract_dict:
        f.write(tract2line(tract,tract_dict[tract])+'\n')


# #### Loading Stuff back in

# In[17]:

with open('tracts.tsv','r') as f:
    lines = f.readlines()
tract_dict = {}
for line in lines:
    tract_dict.update(line2tract(line))
print len(tract_dict)
tract_dict[tract_dict.keys()[10]]

