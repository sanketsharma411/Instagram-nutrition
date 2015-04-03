import numpy as np
from scipy import stats
'''
This file contains Library functions to be used while working with the 16M format
'''
#========================================================================================================#
def loadRegions():
    '''
    Loads the 5 regions in the states and returns a dict with keys as the 5 regions and values as the
    list of state postal ids falling in that region
    5 regions from 'http://parkerwiki0910.pbworks.com/f/1252368970/us%20regions.gif'
    State ids from 'http://50statesinalphabeticalorder.com/images/state_abbreviations_map.png'
    '''
    #Loading the 5 regions
    with open('C:\Users\Shweta\Desktop\CS 8903\FINAL/food_deserts\data\US_5regions.txt','r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    reg_state_dict = {}
    for line in lines:
        if len(line) > 2:
            reg = line
            reg_state_dict[reg] = []
        else:
            reg_state_dict[reg].append(line)
    return reg_state_dict
#========================================================================================================#
## Function to return any column of the passed line of post
def getColumn(lines_of_post,col_num=None):
    '''
    Takes an input the lines of post as specified in 16March format and returns a list of values of a particular column
    Can also pass a list of columns to get a list of lists where each internal list is a list of the columns for a particular line
    col_num can range from 0-28, anything outside throws exception
    '''
    if col_num == None:
        print 'WARNING : No Column Number entered'
        return None
    if hasattr(col_num, '__iter__'):
        # It is an iterable, i.e. multiple columns are requested
        l = []
        for col in col_num: # Obtaining individual columns
            l.append(getColumn(lines_of_post,col))
        return np.column_stack(l).tolist() # Stacking them together
    else:
        if col_num < 0 or col_num > 28:
            raise IndexError('Column Number >| '+str(col_num)+' |< outside range of 0-28')
        else:
            l = []
            for line in lines_of_post:
                l.append(line[col_num])
    return l
#========================================================================================================#
def getNut(lines_of_post,nut_name = None):    
    nut_idx = {'cal':18,'sug':19,'fat':20,'cho':21,'fib':22,'pro':23}
    if type(nut_name) == str:
        if nut_name not in nut_idx:
            raise KeyError('Nutrient Name "'+str(nut_name)+'" is invalid. Use one of [cal|sug|fat|cho|fib|pro]')
        l = getColumn(lines_of_post,nut_idx[nut_name])
        l = [float(x) for x in l]
        return l
    
    elif nut_name == None:
        # Return all nuts
        nut_ids = sorted(nut_idx.values())
    
    elif hasattr(nut_name, '__iter__'):
        # It is an iterable
        # Create a list of the nut_idx which we need and 
        try:
            nut_ids = [nut_idx[nut] for nut in nut_name]
        except KeyError as e:
            raise KeyError('Nutrient Name "'+str(nut)+'" is invalid. Use one of [cal|sug|fat|cho|fib|pro]')
    l = []
    for one_line in getColumn(lines_of_post,nut_ids):
        # Converting each list to float
        l.append(map(float,one_line))
    return l    
#========================================================================================================#
def getCanNames(lines_of_post, ignore_nope_hits = True):
	if ignore_nope_hits: 
		l = []
		for line in lines_of_post:
			if line[24] == '1':
				l.append(line[16].split(';'))
		return l
	else:
		return [x.split(';') for x in  getColumn(lines_of_post,16)]
#========================================================================================================#
VAL_IDX = {'id':0,'user_has_liked':1,'media_type':2,'filter':3,'UTC':4,'IG_URL':5,'user_id':6,'query_tag':7,'tags':8,'MEDIA_URL':9,\
'caption_id':10,'caption':11,'loc':12,'num_likes':13,'num_comm':14,'num_tags':15,'can_matches':16,'id_matches':17,'cal':18,\
'sug':19,'fat':20,'cho':21,'fib':22,'pro':23,'direct_hit':24,'time_zone':25,'time':26,'tract':27,'fd':28}
def getVal(lines_of_post,val_name):
    '''
    Takes as input the value_name and returns the column of that particular value from the lines_of_post
    '''
    if type(val_name) == str:
        if val_name not in VAL_IDX:
            raise KeyError('Nutrient Name "'+str(val_name)+'" is invalid. Use one of ['+str(VAL_IDX.keys())+']')
        l = getColumn(lines_of_post,VAL_IDX[val_name])
        return l
    
    elif val_name == None:
        # By Default Return all nuts
        nut_ids = None
    
    elif hasattr(val_name, '__iter__'):
        # It is an iterable
        # Create a list of the VAL_IDX which we need and 
        try:
            val_ids = [VAL_IDX[nut] for nut in val_name]
        except KeyError as e:
            raise KeyError('Nutrient Name "'+str(nut)+'" is invalid. Use one of '+str(VAL_IDX.keys()))

    return  getColumn(lines_of_post,val_ids)
#========================================================================================================#
def avgNuts(list_of_posts):
    '''
    Based on the 16March line format, give this a set of lines and it returns the average of the 6 nutrients in the order in which they 
    were passed, 
    specifically of the numbers from index 18 to index  23.
    '''
    
    nut_vals = {}
    for post in list_of_posts:
        for i in range(18,24):
            if i not in nut_vals:
                nut_vals[i] = []
            nut_vals[i].append(float(post[i]))
    avgs = []
    for i in nut_vals:
        avgs.append(np.mean(nut_vals[i]))
    return avgs
#========================================================================================================#
def avgPostsPerDay(list_of_posts):
    '''
    Given a list of posts based on 16March line format, this computes the number of posts per day, 
    i.e. total number of distinct days for which we have posts divided by the total number of posts
    
    EDGE CASE : When the total time difference is too small, then extrapolating to a day gives really large numbers
    The crawling wasn't consistent across time, so I am not sure how to interpret this number, maybe look at it
    in comparison with other numbers
    '''
    # Not converting to datetime, as same can be accomplished with strings
    dates = set()
    # Get UTC time
    UTC = [int(time) for time in getVal(list_of_posts,'UTC')]
    # Take difference between the largest and smallest time
    diff = max(UTC) - min(UTC)
    if diff == 0:
        return len(list_of_posts)
    # Convert difference to days

    diff = diff*1.0/86400
    # Divide number of posts by this amount
    return len(list_of_posts)*1.0/diff
    '''
    for post in list_of_posts:
        date = post[-3].split()[0]
        dates.add(date)
    
    return len(list_of_posts)*1.0/len(dates)
    '''
    
#========================================================================================================#
# http://www.samuelbosch.com/2014/05/working-in-lat-long-great-circle.html

from math import radians, degrees, cos, sin, sqrt, atan2, asin, fabs, pi

class Point(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __str__(self):
        return str(self.x)+','+str(self.y)
        
def get_centroid_from_points(points):
    '''
    http://www.geomidpoint.com/example.html 
    http://gis.stackexchange.com/questions/6025/find-the-centroid-of-a-cluster-of-points
    '''
    sum_x,sum_y,sum_z = 0,0,0
    for p in points:
        lat = radians(p.x)
        lon = radians(p.y)
        ## convert lat lon to cartesian coordinates
        sum_x = sum_x + cos(lat) * cos(lon)
        sum_y = sum_y + cos(lat) * sin(lon)
        sum_z = sum_z + sin(lat)
    avg_x = sum_x / float(len(points))
    avg_y = sum_y / float(len(points))
    avg_z = sum_z / float(len(points))
    center_lon = atan2(avg_y,avg_x)
    hyp = sqrt(avg_x*avg_x + avg_y*avg_y) 
    center_lat = atan2(avg_z, hyp)
    return Point(degrees(center_lat), degrees(center_lon))

def getCentroid(list_of_posts):
    '''
    Posts collected in the 16March format
    This returns the centroids of the posts
    i.e. specifically the column 12's first two entries split by ','
    '''
    list_points = []
    for line in list_of_posts:
        lat,lon = [float(i) for i in line[12].split(',')[:2]]
        list_points.append(Point(lat,lon))
    res = get_centroid_from_points(list_points)
    return res.x,res.y
	
#========================================================================================================#
import dateutil.parser
def getDateTime(lines_of_post):
    # First let get the dateTime strings
    dt_list = getVal(lines_of_post,'time')
    # Now lets convert them into datetime objects
    dt_list = [dateutil.parser.parse(dt) for dt in dt_list]
    return dt_list

#========================================================================================================#
def t_test(lines_of_post, val ,distr_by,distr_val = '1',debug = False ):
    '''
    Function performs a binary t-test on val column of the lines_of_post 
    The first distribution in the t-test will be the one for which the distr_by == distr_val, though a few tests suggest it makes no diff
    params: val : The value on which two distributions will be compared, will be converted to float for comparison
            distr_by : column by which we distribute the lines of post into two sets 
            distr_val: value of the column, default = '1' 
                Note: Right now this function is meant to operate right on top of the M16 format, so this value is thus a string
            debug: by default false, will print the length of the two columns
    returns: t : the t-value
             p : the p-value
    '''
    # T-test results are same irrespective of the order
    t_val = [] # the list of items for which distr_by == distr_val
    f_val = [] # EVerything except t_val
    for post in lines_of_post:
        if post[VAL_IDX[distr_by]]  == distr_val:
            t_val.append(float(post[VAL_IDX[val]]))
        else:
            f_val.append(float(post[VAL_IDX[val]]))
    # Now do the t-test between these values
    two_sample_diff_var = stats.ttest_ind(t_val, f_val, equal_var=False);
    if debug:
        print 'Len  =',len(t_val),'|',len(f_val)
        print 'Mean = ',np.mean(t_val),'|',np.mean(f_val)
        print 'STD  = ',np.std(t_val),'|',np.std(f_val)
        print("  t : %.3f  p : %.3f \n" % two_sample_diff_var)
    return two_sample_diff_var
