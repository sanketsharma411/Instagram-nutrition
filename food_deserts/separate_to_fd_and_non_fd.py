
# coding: utf-8

# ### This file takes as input the .US file and based on the entry in the last column, it splits it into .US.fd and .US.nfd
# Format of the .US file is as follows
# -  0-15: post
# - 16-24: nut info
# - 25-28: US info
# 
# The new files have this same format but only with either fd or only non fd posts

# In[1]:

with open('post.txt.nut.US.ALL','r') as f:
    lines = f.readlines()


# In[2]:

fd_nfd_dict = {'0':[], '1':[]}
for line in lines:
    try:
        fd_nfd_dict[line.strip().split('\t')[-1]].append(line)
    except:
        pass
print len(fd_nfd_dict), len(fd_nfd_dict['0']), len(fd_nfd_dict['1'])


# In[3]:

# Writing to food desert file
with open('post.txt.nut.US.nfd','w+') as f:
    for line in fd_nfd_dict['0']:
        f.write(line)
        
# Writing to non-food desert file
with open('post.txt.nut.US.fd','w+') as f:
    for line in fd_nfd_dict['1']:
        f.write(line)        


# In[4]:

x = [len(line.split('\t')) for line in lines]
print set(x)


# In[6]:

x.count(29)


# In[ ]:



