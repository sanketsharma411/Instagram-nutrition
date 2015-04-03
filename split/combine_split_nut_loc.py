
# coding: utf-8

# In[2]:

basepath = '/nethome/ssharma321/split_data_2/split_data//'
BIG_dict = {}
for i in range(39,79):
    filename = basepath+str(i)+'//post.txt.nut.US'
    print filename
    
    with open(filename,'r') as f:
        lines = f.readlines()
    for line in lines:
        BIG_dict[line.split('\t')[0]] = line
    


# In[ ]:

# Writing everything
with open(basepath+'post.txt.nut.US.ALL','w+') as f:
    for post_id in BIG_dict:
        f.write(BIG_dict[post_id])

