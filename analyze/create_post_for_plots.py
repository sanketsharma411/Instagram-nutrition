import sys,os, gc
sys.path.append('/nethome/ssharma321/FINAL/scripts')
from split_lib import *

base_path = '/nethome/ssharma321/split_data'
n = 1
print 'Loading Post'
post_dict = load_split_posts(base_path,n)
gc.collect()
print 'Loading Nut_info Files'
nut_info_lines = load_split_nut_info_lines(base_path, n)
gc.collect()
print 'Loading Nut Info'
post_dict = set_post_dict_nut_info(post_dict, nut_info_lines)
del nut_info_lines
gc.collect()

############### LOADING COMMENTS ###########################
print 'Reading Comments file into memory'
with open('/nethome/ssharma321/comments.txt','r') as f:
	comm_lines = f.readlines()
print len(comm_lines)

# Creating a set of the ids seen before
print 'Discarding all Useless Comments'
id_set = set(post_dict.keys())
# Separating the loaded comments into stuff we want
comm_lines2 = []
count = 0
for line in comm_lines:
	count += 1
	if not count % 200000:	print count
	if line.split('\t')[0] in id_set:
		comm_lines2.append(line)

del comm_lines
		
print len(comm_lines2)


# set_comm_info
print 'Setting Comments Info'
count = 0
for line in comm_lines2:
	count += 1
	if not count % 20000:print count
	post_dict[line.split('\t')[0]].set_comment(line)

############### Loading DateTime info ###########################
with open('post_with_time.txt','r') as f:
        time_lines = f.readlines()
post_time = {}
for line in time_lines:
        post_time[line.strip.split('\t')[0]] = '\t'.join(line.strip.split('\t'))+'\n'
############### Cleaning Stuff ###########################
print 'Cleaning Stuff'

print len(post_dict)

bad_id_set = set()
for post_id in post_dict:
    if not post_dict[post_id].has_nuts :
        bad_id_set.add(post_id)

len(bad_id_set)

for post_id in bad_id_set:
    del post_dict[post_id]

print len(post_dict)

all_posts = set(post_dict.values())

results_path = '/nethome/ssharma321/res_path'
'''
############################POST CAL#######################
post_cal = defaultdict(int)
for post in all_posts:
    post_cal[np.round(post.calories)] += 1

with open(results_path+'//post_cal.txt','w+') as f:
    for cal in sorted(post_cal.keys()):
        f.write(str(cal)+'\t'+str(post_cal[cal])+'\n')
    print 'Done Writing'	

########### LIKES HISTOGRAM #################################
l = []
print '########### LIKES HISTOGRAM #################################'
for post in all_posts:
    l.append(post.likes)
	
c_l = count_list(l)

with open(results_path+'//likes_hist.txt','w+') as f:
    for num_likes in sorted(c_l.keys()):
        f.write(str(num_likes)+'\t'+str(c_l[num_likes])+'\n')
    print 'Done Writing'

############ Cummulative LIKES CALORIES #####################
likes_cal = defaultdict(int)
print '############ Cummulative LIKES CALORIES #####################'
for post in all_posts:
    likes_cal[np.round(post.calories)] += post.likes

with open(results_path+'//likes_cal.txt','w+') as f:
    for cal in sorted(likes_cal.keys()):
        f.write(str(cal)+'\t'+str(likes_cal[cal])+'\n')
    print 'Done Writing'


########## AVG LIKES CALORIES #######################
likes_cal = defaultdict(int)
for post in all_posts:
    likes_cal[np.round(post.calories)] += post.likes

print '############ Cummulative LIKES CALORIES #####################'

for cal in likes_cal:
    likes_cal[cal] = likes_cal[cal]*1.0/post_cal[cal]

with open(results_path+'//avg_likes_cal.txt','w+') as f:
    for cal in sorted(likes_cal.keys()):
        f.write(str(cal)+'\t'+str(likes_cal[cal])+'\n')
    print 'Done Writing'

######### NUM COMMENTS VS CALORIES #####################
comm_cal = defaultdict(int)	
print '######### NUM COMMENTS VS CALORIES #####################'

for post in all_posts:
    comm_cal[np.round(post.calories)] += post.get_num_comments()

with open(results_path+'//comm_cal.txt','w+') as f:
    for cal in sorted(comm_cal.keys()):
        f.write(str(cal)+'\t'+str(comm_cal[cal])+'\n')
    print 'Done Writing'	
'''
######### Everything #####################
#with open(results_path+'//post_cal.txt','w+') as f:
with open(results_path+'//post_time_for_plots.txt','w+') as f:
	for post in all_posts:
		st = post.id +'\t'
		st += post.tags+'\t'
		st += str(post.likes) +'\t'
		st += str(post.get_num_comments())+'\t'
		st += str(post.calories) +'\t'
		st += str(post.fat) +'\t'
		st += str(post.protein)+'\t'
		st += post_time[post.id]
		f.write(st)
		
print 'HAASH FINALLY'
	


	
	
	
	
	
	
	
	
	
