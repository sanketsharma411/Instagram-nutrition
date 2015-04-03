'''
This file is meant to parse post JSON returned from the API, and store it nicely, in the format defined below.
It is a subset of the functions in  InstaLib.py, separated out specifically to only parse the post and return the data nicely ;)
[Built for Stevie]
'''
import re
#######################################################	
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
#######################################################	
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
#######################################################
def parse_post(instance,tag=''):
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
		