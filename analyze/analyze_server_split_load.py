import os,sys
sys.path.append('/nethome/ssharma321/FINAL/scripts')
from analyze_utils import *
from split_lib import *
#from matplotlib import pyplot as plt
#results_path = 'C:/Users/Shweta/Desktop/CS 8903/FINAL/for_server/test_results'
#base_path = 'C:\\Users\\Shweta\\Desktop\\CS 8903\\FINAL\\for_server\\split_data'
base_path = '/nethome/ssharma321/split_data'
results_path = '/nethome/ssharma321/res_path'
n = 2
# loading the  post_info
post_dict = load_split_posts(base_path,n)
print '========================================== POST_DICT [Original] = '+str(len(post_dict))

# Removing all the posts with caloric value greater than 800 kcal or no caloric info
bad_id_set = set()
for post_id in post_dict:
    if post_dict[post_id].calories > 800 or not post_dict[post_id].has_nuts:
        bad_id_set.add(post_id)

print len(post_dict)
        
# Now remove them from the dict
for post_id in bad_id_set:
    del post_dict[post_id]
print len(post_dict)

# Converting the post_dict to a set of only the post_objects
all_posts = set(post_dict.values())
print len(all_posts)


#####################################################################
# Now Histogram of calories vs post
# X : calories
# Y : num posts
# Use this plotting method always : Create a dict of type {X:Y}
# method is dumb but allows it to be extended and played around with easily
post_cal = defaultdict(int)
for post in all_posts:
    post_cal[np.round(post.calories)] += 1
#plot_dict(post_cal,'rx')
####################SAVE FIGURE HERE

# Saving this dict into the results folder
with open(results_path+'//post_cal.txt','w+') as f:
    for cal in sorted(post_cal.keys()):
        f.write(str(cal)+'\t'+str(post_cal[cal])+'\n')
    print 'Done Writing'

####################################################################
# Likes vs posts
l = []
for post in all_posts:
    l.append(post.likes)
c_l = count_list(l)
#plt.plot(c_l.keys(),c_l.values(),'rx')
#plt.xlim([])
#plt.show()
####################SAVE FIGURE HERE

# Saving this dict into results folder
with open(results_path+'//likes_hist.txt','w+') as f:
    for num_likes in sorted(c_l.keys()):
        f.write(str(num_likes)+'\t'+str(c_l[num_likes])+'\n')
    print 'Done Writing'


####################################################################
likes_cal = defaultdict(int)
# Creating the dict
for post in all_posts:
    likes_cal[np.round(post.calories)] += post.likes
# Plotting it
#pltplot(likes_cal.keys(),likes_cal.values(),'rx')
#plt.ylim([0,500])   # I guess 500 is good for this sample data, might have to do some math here to get the 95% confidence interval

# Now lines for mean, mean+sd, mean-sd
mean = np.mean(likes_cal.values())
sd = np.std(likes_cal.values())

# Line for Mean
#plt.plot([0,max(likes_cal.keys())],[mean,mean],color='b')
# Line for Mean + sd
#plt.plot([0,max(likes_cal.keys())],[mean+sd,mean+sd],color='g')
# Line for Mean - sd
#plt.plot([0,max(likes_cal.keys())],[mean-sd,mean-sd],color='g')
#plt.show()
####################SAVE FIGURE HERE

with open(results_path+'//likes_cal.txt','w+') as f:
    for cal in sorted(likes_cal.keys()):
        f.write(str(cal)+'\t'+str(likes_cal[cal])+'\n')
    print 'Done Writing'
####################################################################
likes_cal = defaultdict(int)
# Creating the dict
for post in all_posts:
    likes_cal[np.round(post.calories)] += post.likes

# Normalizing the likes by the number of posts at that caloric value
for cal in likes_cal:
    likes_cal[cal] = likes_cal[cal]*1.0/post_cal[cal]

# Plotting it
#plt.plot(likes_cal.keys(),likes_cal.values(),'rx')
#plt.ylim([0,100])   # I guess 500 is good for this sample data, might have to do some math here to get the 95% confidence interval

# Now lines for mean, mean+sd, mean-sd
mean = np.mean(likes_cal.values())
sd = np.std(likes_cal.values())

# Line for Mean
#plt.plot([0,max(likes_cal.keys())],[mean,mean],color='b')
# Line for Mean + sd
#plt.plot([0,max(likes_cal.keys())],[mean+sd,mean+sd],color='g')
# Line for Mean - sd
#plt.plot([0,max(likes_cal.keys())],[mean-sd,mean-sd],color='g')
#plt.show()
####################SAVE FIGURE HERE

with open(results_path+'//likes_cal.txt','w+') as f:
    for cal in sorted(likes_cal.keys()):
        f.write(str(cal)+'\t'+str(likes_cal[cal])+'\n')
    print 'Done Writing'
#####################################################################
# Creating the required dictionary
comm_cal = defaultdict(int)
for post in all_posts:
    comm_cal[np.round(post.calories)] += post.get_num_comments()
# mean
mean = np.mean(comm_cal.values())
# sd
sd = np.std(comm_cal.values())

# Plotting the dict
#plt.plot(comm_cal.keys(),comm_cal.values(),'bx')
# lines for mean+sd, mean, mean-sd
#plt.plot([0,max(comm_cal.keys())],[mean+sd,mean+sd],color='r') # mean+sd
#plt.plot([0,max(comm_cal.keys())],[mean,mean],color='g') # mean
#plt.plot([0,max(comm_cal.keys())],[mean-sd,mean-sd],color='r') # mean-sd
#plt.show()
####################SAVE FIGURE HERE
# Saving the dict to memory
with open(results_path+'//comm_cal.txt','w+') as f:
    for cal in sorted(comm_cal.keys()):
        f.write(str(cal)+'\t'+str(comm_cal[cal])+'\n')
    print 'Done Writing'
