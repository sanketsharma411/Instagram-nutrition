
Specific Acce
	This file has general and specific accessor functions, 
	The difference is that the specific accessor functions will return the values in their respective format
	While the general functions are going to return only the string values as read from the post.txt.nut.US file
	Note : The specific accessor functions are added only when required, so you may not have specific access to all
		the values.
	List of stuff with specific access:
	getNut -> Nutrients as floats
	getCanNames -> Canonical Names as list of elements
	getDateTime -> Date Time object
	

Function description
loadRegions()
	Loads the 5 regions in the states and returns a dict with keys as the 5 regions and values as the
    list of state postal ids falling in that region

getColumn(lines_of_post,col_num=None):
    Takes an input the lines of post as specified in 16March format and returns a list of values of a particular column
    Can also pass a list of columns to get a list of lists where each internal list is a list of the columns for a particular line
    col_num can range from 0-28, anything outside throws exception

	
getNut(lines_of_post,nut_name = None)
	nut_idx = {'cal','sug','fat','cho','fib','pro'}
	Converts the nut value to float before returning
	
getCanNames(lines_of_post, ignore_nope_hits = True)
	Returns the canonical names, ignoring the nope_hits
	<Add this functionality to the generic accessor, of returning stuff only if some particular value is 0>

avgNuts(list_of_posts):
	Based on the 16March line format, give this a set of lines and it returns the average of the 6 nutrients in the order in which they 
    were passed, specifically of the numbers from index 18 to index  23.
    
avgPostsPerDay(list_of_posts):
    Given a list of posts based on 16March line format, this computes the number of posts per day, 
    i.e. total number of distinct days for which we have posts divided by the total number of posts
	EDIT : WORK IN PROGRESS
   
getCentroid(list_of_posts):
	This returns the centroids of the posts
    i.e. specifically the column 12's first two entries split by ','

getDateTime(lines_of_post):
	Specific Accessor function to access the datetime and return a list of datetime objects

	
{'id':0,\'user_has_liked':1,\'media_type':2,\'filter':3,\'UTC':4,\'IG_URL':5,\'user_id':6,\'query_tag':7,\'tags':8,\'MEDIA_URL':9,\'caption_id':10,\
'caption':11,\'loc':12,\'num_likes':13,\'num_comm':14,\'num_tags':15,\'can_matches':16,\'id_matches':17,\'cal':18,\'sug':19,\'fat':20,\
'cho':21,\'fib':22,\'pro':23,\'direct_hit':24,\'time_zone':25,\'time':26,\'tract':27,\'fd':28\}
