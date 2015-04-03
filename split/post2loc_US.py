
# coding: utf-8

# In[1]:

import datetime, pytz
from tzwhere import tzwhere 
w = tzwhere.tzwhere()
from dateutil import parser
import urllib2,json

base_path = '/nethome/ssharma321/split_data/1/'
##########################################################################################
##########################################################################################
##########################################################################################
i=0
##########################################################################################
##########################################################################################
##########################################################################################
post_filename = base_path+'//'+str(i)+'//post.txt'
print post_filename
fd_filename = '/nethome/ssharma321/FINAL/food_deserts/data/food_deserts_ids.txt'
## Loading the food deserts data
with open(fd_filename,'r') as f:
    lines = f.readlines()
food_deserts_ids = [line.strip() for line in lines]
food_deserts_ids = set(food_deserts_ids)

############################################################################################################################################\
def get_loc_time(UTC,lat,lon):
    '''
    Given a lat lon, this converts the passed UTC time into the local time at that lat lon and the timezone in which the lat lon falls
    '''
    UTC_time = float(UTC)
    lat = float(lat)
    lon = float(lon)
    # Getting the local timezone Name
    local_tz_name = w.tzNameAt(lat,lon)
    if local_tz_name == None:
        has_loc_time = False
        return -1,-1
    
    # Converting back from the timestamp
    dt = datetime.datetime.utcfromtimestamp(UTC_time)
    # Saving the original unlocalized time
    dt_og = dt
    # Localizing the time, i.e. attaching the UTC information
    dt = pytz.utc.localize(dt)
    # Getting the local timezone
    local_tz = pytz.timezone(local_tz_name)
    # Getting the offset from UTC to this timezone
    offset = dt.astimezone(local_tz).utcoffset()
    # Adding the offset to the original time to get the new localized time
    # Need to subtract one hour from this time because it is off by one hour, i.e.
    # It adds an extra hour
    return local_tz,dt_og+offset

# Given lat long, write the tract id and if it is a  food desert or not, and if it is in the US or not
def getTract(lat,lon):
    '''
    Returns the tract_id and 1 or 0 indicating if it is a Food desert or not
    If we could not find a Tract id we asssume that this lat lon is outside US.
    Possible Return values
    In US & food desert     => tract_code,1
    In US & not food desert => tract_code,0
    Not in US               => -1,-1
    Tract Code is a string
    '''
    lat = float(lat)
    lon = float(lon)
    if lat >= 16 and lat <= 72 and lon <= -63.57 and lon >= -172:
        # API request for tract id
        query = 'http://data.fcc.gov/api/block/find?format=json&latitude='+str(lat)+'&longitude='+str(lon)+'&showall=False'
        tract_code = json.load(urllib2.urlopen(query))["Block"]["FIPS"]
        if tract_code != None:
            if tract_code[:11] in food_deserts_ids:
                # If this is a food desert
                return tract_code,1
            else:
                # Not a food desert
                return tract_code,0
        else:
            # In the bounding box but not in the US
            return -1,-1
    else:
        # Not in the bounding box 
        return -1,-1
#####################################################################################################################################################

# In[8]:


# In[33]:
with open(post_filename,'r') as f:
    lines =f.readlines()
f_loc = open(post_filename+'.loc','w+')
f_US = open(post_filename+'.US','w+')


# In[34]:

for line in lines:
    og_line = line
    line = line.split('\t')
    if len(line) == 16:
        loc = line[12].split(',')
        if loc[0] != 'NA':
            UTC_time = line[4]
            lat = loc[0]
            lon = loc[1]            
            tzinfo, time = get_loc_time(UTC_time,lat,lon)
            loc_line = og_line.strip()+'\t'+str(tzinfo)+'\t'+str(time)+'\n'
            if tzinfo != -1 and time != -1:
                f_loc.write(loc_line)
            # Now on to the US based locations
            tract,fd = getTract(lat,lon)
            if tract != -1:
                US_line = loc_line.strip() +'\t'+tract+'\t'+str(fd)+'\n'
                f_US.write(US_line)


# In[35]:

f_loc.close()
f_US.close()

# In[3]:


# In[7]:

# Now on to use these functions to set the required values in the post file
# Load Posts
# if has lat lon
#     Get tzone and local time
#          Write to file
#     if in us
#         get tract and fd or not
#         Write to file



''' Reading stuff back
with open(post_filename+'.US','r') as f:
    loc_lines = f.readlines()
for line in loc_lines:
    line = line.split('\t')
    print line[16]
    print parser.parse(line[17])
    print line[17]
    print line[18]
    print line[19]
'''    


