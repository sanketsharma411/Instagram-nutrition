'''
Created 26 Feb
File contains location related helper functions.
Getting the local timezone given the lat,lon and UTC requires us to load
the tzwhere library which takes a lot of memory ~600MB so use the
library only in this file i.e. all datetime jobs to be done here,
and do not load this file unless necessary.
'''
import datetime, pytz
from tzwhere import tzwhere 
w = tzwhere.tzwhere()
from dateutil import parser
import urllib2,json

#######################################################################
################# Get Local Time    ###################################
################# Given UTC,Lat,lon ###################################
#######################################################################
def getLocalTime(UTC,lat,lon):
    '''
    Given a lat lon, this converts the passed UTC time into the local time at that lat lon
    Returns local_tz : tzinfo object of the timezone from the lat lon
            dt_og+offset: Local Time at lat lon
    if return = -1,-1 => No Matching Time zone found, does not throw an error !
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
#######################################################################
################# Get US Tract id      ################################
################# & Food Desert or not ################################
################# Given Lat,lon        ################################
#######################################################################

#######################################################################
# Loading the list of food deserts
#######################################################################
print 'Loading Food Deserts Data'
#fd_filename = '/nethome/ssharma321/FINAL/food_deserts/data/food_deserts_ids.txt'
fd_filename = 'C:/Users/Shweta/Desktop/CS 8903/FINAL/food_deserts/data/food_deserts_ids.txt'
with open(fd_filename,'r') as f:
    lines = f.readlines()
food_deserts_ids = set([line.strip() for line in lines])
print 'Loading Food Deserts Data !! DONE !!'
#######################################################################
# The Function
#######################################################################
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

