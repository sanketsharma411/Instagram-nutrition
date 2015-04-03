#from instagram.client import InstagramAPI
import numpy as np
#import matplotlib.pyplot as plt
import urllib2,time,re, operator, pickle,json, sys, operator, datetime, pprint, pickle, os.path, random
from collections import defaultdict
# For the tag cloud
#from pytagcloud import create_tag_image, make_tags
#from pytagcloud.lang.counter import get_tag_counts
"""
==========Instagram Library Functions===========================
This file contains all the functions which ever need to be created, so, write all the functions
over here, and import this file
"""
def setup_api():
    """
    Creates an Instagram API object, with the predefined credentials, and returns the
    API object and the ACCESS_TOKEN
    """
    print '=========Initialization     ===================='
    CLIENT_ID = '155d1dc6f29d4806acee4f651630dc52'
    CLIENT_SECRET = '586f618280ad4ba8abc45ed9cd96fc54'
    REDIRECT_URI = 'http://www.s-udacity.appspot.com'
    ACCESS_TOKEN = '1479030016.155d1dc.81cce70e60d9465e9a520b636a6566e5' # For sanketonly
    # To get a new access token, go to 
    # print 'https:/  /instagram.com/oauth/authorize/?client_id='+CLIENT_ID+'&redirect_uri='+REDIRECT_URI+'&response_type=token'
    # sanketonly : user_id = 1479030016

    #return InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET),ACCESS_TOKEN
    return ACCESS_TOKEN

###########################################################################################    
def parse_post(instance,tag):
    user = ''
    s = ''
    ##############Initial#####################################
    post_id = instance['id']
    s += str(post_id)
    s += '\t' + str(instance['user_has_liked'])
    s += '\t' + str(instance['type'])
    s += '\t' + str(instance['filter'])
    s += '\t' + str(instance['created_time'])
    s += '\t' + str(instance['link'])
    
    
    ##############User######################################
    # Now on to the main user who has posted the image
    s += '\t' + instance['user']['id']
    user += parse_user(instance['user'],post_id,'POST')


    #############Tags##########################################
    # Adding section for printing the queried tag
    s += '\t'
    s += tag
    #############Tags##########################################
    # For tags, we separate indivuidual tags by commas,
    s +='\t'
    for one_tag in instance['tags']:
        s += clean_text(one_tag) + ','
    s = s[0:len(s)-1]

    
    ############Image_URL######################################
    s += '\t' + str(instance['images']['standard_resolution']['url'])

    ##############Caption###############	#######################
    # Now on to caption/ description of the photo
    if instance['caption'] != None:
        s += '\t' + str(instance['caption']['id'])
        s += '\t' + clean_text(instance['caption']['text'])
    else:
        s += '\t' + 'NA' + '\t' + 'NA'
        
    ##############Location######################################
    # Now on to location
    if instance['location'] != None:
        try:
            s += '\t' + str(instance['location']['latitude']) + ','
            s += str(instance['location']['longitude']) + ','
            try:
                s += clean_text(instance['location']['name']) + ','
                s += str(instance['location']['id'])
            except KeyError:
                s += 'NA,NA'
        except KeyError:
            s += 'NA,NA'
    else:
        s +=  '\t' + 'NA,NA,NA,NA'

    ##########Comments#########################################
    c = ''
    s += '\t' + str(instance['comments']['count'])
    for comment in instance['comments']['data']:
        c += post_id    
        c +=  '\t' + str(comment['id'])
        c +=  '\t' + str(comment['created_time'])
        c +=  '\t' + clean_text(comment['text'])
        c +=  '\t' + comment['from']['id']
        c +=  '\n'
        user += parse_user(comment['from'],post_id,'COMMENT')
        
    ##########Likes#############################################
    l = ''
    s += '\t' + str(instance['likes']['count'])
    l += post_id + '\t'
    l += str(instance['likes']['count']) + '\t'
    
    for user_info in instance['likes']['data']:
        l += user_info['id'] + ','
        user += parse_user(user_info,post_id,'LIKE')
        
    l = l[0:len(l)]
    l += '\n'
    
    ##########UsersInPhoto####################
    # Now on to number of users in the photo
    u_in_photo = ''
    if instance['users_in_photo'] != None:
        s += '\t' + str(len(instance['users_in_photo']))
        for info in instance['users_in_photo']:
            u_in_photo += post_id
            u_in_photo += '\t' + str(info['position']['x'])
            u_in_photo += '\t' +str(info['position']['y'])
            u_in_photo += '\t' + info['user']['id']
            u_in_photo += '\n'
            user += parse_user(info['user'],post_id,'TAG')
    else:
        s += '\t' + '0'
    s+= '\n'
    return s,c,l,u_in_photo,user

###########################################################################################
def get_posts_to_file(tag_list,n_requests,ACCESS_TOKEN,sleep = 0):
    '''
    Puts in n_requests for each tag, with time of sleep betweent two requests
    Creates following text files:
        post.txt
        comments.txt
        likes.txt
        users_in_photo.txt
    '''
    #0) Initialize required parameters
    query = "https://api.instagram.com/v1/tags/"
    request = "/media/recent?access_token="
    tag_dict = defaultdict(int)
    t0 = time.time()
    t1 = t0
    tot_reqs = 0
        
    f_post = open('post_Feb7.txt','a')
    f_comments = open('comments_Feb7.txt','a')
    f_likes = open('likes_Feb7.txt','a')
    f_users = open('users_Feb7.txt','a')
    f_users_in_photo = open('users_in_photo_Feb7.txt','a')

    # Initializing parameters to count the number of posts each seed tag
    seed_tag_count = defaultdict(int)
    seed_tag_next_url = {}
    # Now check if any previous data file exists
    if not os.path.exists('crawl_data'):
        with open('crawl_data','w+') as f:
            pickle.dump(seed_tag_count,f)
            pickle.dump(seed_tag_next_url,f)
    with open('crawl_data','r') as f:
        seed_tag_next_url = pickle.load(f)
        seed_tag_count.update(pickle.load(f))
    #seed_tag_next_url = {}
    #seed_tag_count = defaultdict(int)
    
    
    '''
    seed_tag_count = dict.fromkeys(tag_list,0)
    # Initializing params to keep track of the next_url for each seed tag
    seed_tag_next_url = dict.fromkeys(tag_list)
    '''
    # Initializing the interim status
    with open('interim_status.txt', 'a') as f:
            f.write ('\n=========================='+str(datetime.datetime.now()) + '====================\n')
    # Initializing the next_url_dict
    
    #########################################################################################
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #########################################################################################
    # Getting some 'int object has no attribute timeout' error at the start of a new crawl ??
    # That was to check if you have read the instructions or not, Sucker! # # # # # # # # # #
    #########################################################################################
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Uncomment the next 2 lines                    #########################################
    # For all the seed tags, make one request                   #############################
    # Delete the InstaLib.pyc file and Comment the next 2 lines #############################
    # Continue with the rest of the requests        #########################################
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #for tag in tag_list:
    #    seed_tag_next_url[tag] = query + tag + request + ACCESS_TOKEN + '&count=' + str(32)
    # Now for actually putting in requests
    for i in range(n_requests):
        # Update the interim_status file
        update_interim_status_file(seed_tag_count,seed_tag_next_url)

        for tag in tag_list :
            print tag
            try:
                url = seed_tag_next_url[tag]
            except KeyError:
                seed_tag_next_url[tag] = query + tag + request + ACCESS_TOKEN + '&count=' + str(32)
                seed_tag_count[tag] = 0
                url = seed_tag_next_url[tag]
            seed_tag_count[tag] += 1
            #   define p,c,l,u:
            #   These will keep a record of the parsed returned JSON i
            p = '';c = '';l = '';users = '';u_in_photo = ''

            tot_reqs += 1                          # Keeping a count of the total requests
            try:
                response = urllib2.urlopen(url)
                data = json.load(response)
                url = data['pagination']['next_url']
                seed_tag_next_url[tag] = url

            except (urllib2.HTTPError) as e:
                update_interim_status_file(seed_tag_count, seed_tag_next_url, '##############################################HTTP Error##############################################')
                print 'HTTP ERROR OCCURRED'
                continue
				
            except (KeyError) as e:
                update_interim_status_file(seed_tag_count, seed_tag_next_url, '##############################################'+str(e)+'##############################################')
                #end_crawl(2, data, seed_tag_count, seed_tag_next_url)
                print 'KeyError Occurred, yet we continue'
                continue
            
            except Exception, e:
                #end_crawl(3,e)
                update_interim_status_file(seed_tag_count, seed_tag_next_url, '##############################################'+str(e)+'##############################################')
                print '##############################################some random error occurred here, yet we continue##############################################'
                print e
                #end_crawl(3,e, seed_tag_count, seed_tag_next_url)
                continue
             
            print str(tot_reqs) + ': Time ' + '%.2f' %(time.time()-t1)\
            +'s '+ ' | Total Time = ' +'%.2f' %(time.time()-t0) + " | Tag: "\
            + tag + " | Requests Done :  "+str(seed_tag_count[tag]) +"/"+str(n_requests)
            t1 = time.time()

            #   for each instance in data
            for instance in data['data']:
                #   get new p,c,l,u and update the old ones.
                    p_temp,c_temp,l_temp,u_in_photo_temp,users_temp = parse_post(instance,tag)
                #   Add it to the old p,c,l,u
                    p += p_temp;                    c += c_temp;                    l += l_temp
                    u_in_photo += u_in_photo_temp;  users += users_temp
            #   write all of the data to the file
            f_post.write(p + '\n');            f_comments.write(c+ '\n');            f_likes.write(l+ '\n')
            f_users_in_photo.write(u_in_photo+ '\n');            f_users.write(users+ '\n')
            
            #   Now sleep for some time before putting in the next reques
            time.sleep(sleep)

    #9) Lets end everything here
    f_post.close();    f_comments.close();    f_likes.close();    f_users_in_photo.close();    f_users.close()
    status_at_end = 'Graceful exit after ' + str(tot_reqs) + ' Steps \nAnd a total time of ' + str(time.time()-t0) + ' secs'
    end_crawl(0, status_at_end, seed_tag_count, seed_tag_next_url)
    return 0

###########################################################################################
# This is now converted into the better function : get_posts_to_file
def get_info_tags(tag_list,n_requests,ACCESS_TOKEN,sleep = 0):
    """
    Tag based search for relate tags in instagram posts
    tag_list = list of tags for which data is to be collected from Instagram
    n_requests = Number of requests for each tag.
        Each request is replied with 32 responses
    ACCESS_TOKEN = The Access token reequired for Authorization
    sleep = Time to sleep,
        Instagram allows only 5000 requests per access token per hour, so to stay within 
        limits, any sleep time greater than 0.4 seconds is fine.

    Returns 
        frequency-sorted list of the tags appearing with this one
    &   the dictionary of the associated tags and their counts
    &   the last JSON response
    """

    query = "https://api.instagram.com/v1/tags/"
    request = "/media/recent?access_token="
    tag_dict = defaultdict(int)
    t0 = time.time()
    t1 = t0
    tot_reqs = 0
    print '============Start==================' + str(t0)
    if type(tag_list) != 'list':
        tag_list = [tag_list]
        
    for q_tag in tag_list:
        url = query + q_tag + request + ACCESS_TOKEN + '&count=' + str(32)
        for i in range(n_requests):
            tot_reqs += 1                          # Keeping a count of the total requests
            print url
            data = json.load(urllib2.urlopen(url))
            url = data['pagination']['next_url']
            print str(tot_reqs) + ': Time ' + '%.2f' %(time.time()-t1)\
            +'s '+ 'Total Time = ' +'%.2f' %(time.time()-t0) + "  " + q_tag + "-"+str(i+1)
            t1 = time.time()          
            time.sleep(sleep)    
        for index in range(len(data['data'])):
            # Now each dict accessed by data['data'][index] is one response
            for tag in data['data'][index]['tags']:
                tag_dict[tag] += 1
        
        sorted_tag_dict = sorted(tag_dict.iteritems(), key=operator.itemgetter(1))
    print  '============End==================' + str(time.time())
    return sorted_tag_dict, tag_dict, data
    
    
#############################################################################################
'''
def tag_cloud(d,filename="tag_cloud",size_x = 900, size_y = 600):
    """
    d = List of words and their frequency for creating a tag cloud    
    filename = The path/name of the file at which the tag cloud is to be saved
    Function to create a tag Cloud from the dictionary passed in as
    """
    print 'Creating a tag Cloud at ' + filename +'.png'
    tags = make_tags(d[0:len(d) - 1], maxsize=120)
    create_tag_image(tags, filename +'.png', size=(size_x, size_y), fontname='Cardo')
    print 'DONE !! Creating a tag Cloud at ' +filename+'.png'
'''
#############################################################################################
def clean_text(st):
# Function to take care of bad text
# Encoding to ASCII to take care of unicodeEncodeError
    st = st.encode('ascii', 'ignore')
    # st.encode('ascii','ignore') => Ignore all non unicode characters
    # st.encode('ascii','replace') => Replace all non unicode characters with ?
    # st.encode('ascii','strict') => Does not encode instead throws the UnicodeEncodeError
# Removing multiple spaces characters (\t, \n, \r, etc) so that they do not interfere while storing in a tab seperated values file format
    st = re.sub('\s',' ',st)
    return str(st)
#############################################################################################
#def parse_user(st):
# Function to parse through the user field
# Do not know how to work with the website and bio, so have left them for now
# https://api.instagram.com/v1/users/user_id/?access_token=ACCESS-TOKEN
# The above gives us all the information about the user with user_id
#    return str(st['id']) + '\t' +str(st['username'])+'\t' +str(clean_text(st['full_name'])) +'\t' + str(st['profile_picture'])
################################################################################################
def parse_user(st,post_id,activity):
    user_info = str(st['id']) + '\t' +str(st['username'])+'\t' +str(clean_text(st['full_name'])) +'\t' + str(st['profile_picture']) + '\t'

    try:
        if st['bio'] != '':
            user_info += st['bio'] + '\t'
        else:
            user_info += 'NA' + '\t'
    except KeyError: user_info += 'NA' + '\t'

    try: 
        if st['website'] != '':
            user_info += st['website'] + '\t'
        else:
            user_info += 'NA' + '\t'
    except KeyError: user_info += 'NA' + '\t'

    user_info += str(post_id)+'\t'
    user_info += activity + '\n'

    return user_info
        
################################################################################################
def end_crawl(end_code, end_data, seed_tag_count, seed_tag_next_url):
# Function to end the program and display the status at end on the screen, and also print it on a file Status.txt
# This is supposed to handle all the bad exits
#######End Codes
    # end_code = 0 => Good Exit and print the concluding statement to status.txt
    if end_code == 0:
        end_status =  ' Graceful end of the crawl, with the following status:' +'\n' + str(end_data)
        print end_status
        update_end_status_file(end_status,seed_tag_count, seed_tag_next_url)
        

    # end_code = 2 => Bad Exit, and prodblem is in the response JSON
    elif end_code == 2:
        print 'Problem in the Response from Instagram'
        # Now the end_data is the parsed JSON we have recieved in reply
        end_status = 'Problem in the Response from Instagram \t'
        # Now we see if the returned response was JSON or not, if it is JSON, we print it nicely
        if type(end_data) == dict:
            for key in data:
                print data[key]
                end_status += str(key) + ' : ' + str(data[key]) + '\n'
        else:
            print 'Returned response is not JSON'
            end_status += 'Returned response is not JSON, rather it is this\n================\n' + str(end_data)+'\n================\n'
        update_end_status_file(end_status,seed_tag_count, seed_tag_next_url)

    elif end_code == 3:
        print 'some ugly error'
        print ' here\'s the error code and its related details: + \n' + str(end_data)
        end_status = 'some ugly error' + '\t' + 'here\'s the error code and its related details: + \n' + str(end_data)

        update_end_status_file(end_status,seed_tag_count, seed_tag_next_url)
        
    else:
        print 'BAD EXIT !! SOMETHING SOMEWHERE WENT WRONG!!! LOOK AT THE NEXT LINE AND FIGURE IT OUT'
        end_status += 'BAD EXIT !! SOMETHING SOMEWHERE WENT WRONG!!! LOOK AT THE NEXT LINE AND FIGURE IT OUT \t'
        print end_data
        update_end_status_file(end_status+'\n'+end_data,seed_tag_count, seed_tag_next_url)
#############################Creating the final status.txt and other files as described below
#   status.txt = >  Final status of the crawl, the number of steps taken, and the total work done
#   seed_tag_count.txt = > The number of responses collected for each seed_tag
#   seed_tag_next_url.txt = > The next url for each seed_tag, use this for starting new crawls, and to initialize  the dictionary seed_tag_next_url
#   Also pickle both of these to 'end_status' named file
def update_end_status_file(end_data,seed_tag_count, seed_tag_next_url):
    pp = pprint.PrettyPrinter(indent=4)
    with open('status.txt','w') as f:
        f.write(str(datetime.datetime.now()) + '\n' + str(end_data)+'\n')
        f.write('=============Tag Counts==================\n')
        f.write(pp.pformat(seed_tag_count))
        f.write('\n=============Next URL==================\n')
        f.write(pp.pformat(seed_tag_next_url))

    with open('crawl_data','w') as f:
        pickle.dump(seed_tag_next_url,f)
        pickle.dump(seed_tag_count,f)
        f.close()
        
                    
# ########################### Function to update the interim status
def update_interim_status_file(seed_tag_count,seed_tag_next_url, text = ''):
    pp = pprint.PrettyPrinter(indent=1, width=2)
    with open('interim_status.txt', 'a') as f:
        f.write(str(datetime.datetime.now()) + '\n');
        f.write(str(text));
        f.write(str(pp.pformat(dict(seed_tag_count)))+ '\n');
        f.write(str(pp.pformat(dict(seed_tag_next_url))) + '\n')
        f.write('======================================Total Requests Made = '+str(sum(seed_tag_count.values()))+'=========================================\n')

#############################Sorting Dictionaries
def sort_dict(dictionary):
    sorted_dict = sorted(dictionary.items(), key=operator.itemgetter(1))
    sorted_dict.reverse()
    return sorted_dict
    
######################Plotting only the values of the Dictionaries 
def plot_dict_values(dictionary,args=None):
    x = np.arange(len(dictionary))
    y = dictionary.values()
    plt.plot(x,y,args) 
######################Plotting Dictionaries 
'''
def plot_dict(dictionary,args):
    x = dictionary.keys()
    y = dictionary.values()
    plt.plot(x,y,args) 
    plt.show()
'''
#####################Counting number of repititions of items in a list
def count_list (l):
    d = defaultdict(int)
    for element in l:
        d[element] += 1
    return dict(d)
#####################Printing  a list nicely
def print_list(l,sep):
    '''
    Returns the elements of l in a 'sep' separated value string
    You have to take care of the
    '''
    st = ''
    for element in l:
        st += str(element)+sep
    return st.strip(sep)
################### Read the given file
def read_lines(filename):
    with open(filename,'r') as f:
        lines  = f.readlines()
    return lines

################### Print Random Element from a dict
def get_rand_element(d):
    i = random.randint(0,len(d))
    return d[d.keys()[i]]
