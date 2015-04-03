
# coding: utf-8

# In[2]:

import os
#basepath = 'C:/Users/Shweta/Desktop/CS 8903/FINAL/labs/combine multiple .US files//'
basepath = '/nethome/ssharma321/split_data//'


# ### Step 1 : Load the original file 

# In[18]:

outputFile = 'post.txt.nut.US'
id_set = set()
if os.path.isfile(basepath+outputFile):
    print 'Previous posts exist'
    print 'Loading file in r mode'
    with open(basepath+outputFile,'r') as f:
        lines = f.readlines()
    print 'Done Loading'
    print 'Generating  id_list'
    for line in lines:
        post_id =  line.split('\t')[0]
        if post_id not in id_set:
            id_set.add(post_id)
    print 'Generating  id_list !! DONE !!'
    print 'Already Completed ',len(id_set),' posts'
    ################# ALSO LOAD PREVIOUS END STATUS FILE
else:
    print ' No Previous posts exist'
    print 'Creating file'
    with open(basepath+outputFile,'w+') as f:
        pass
    print 'Done Creating the file'


# In[19]:

clean_lines = []
line_count = 0
clean_count = 0
bad_count = 0
for i in range(0,3):
    filename = basepath+'//'+str(i)+'//post.txt.nut.US'
    print filename
    try:
        with open(filename,'r') as f:
            lines = f.readlines()
    except:
        print 'File Does Not Exist'
        continue
    print len(lines)
    for line in lines:
        line_count += 1
        line_og = line
        line = line.split('\t')
        if len(line) == 29 and line[0] not in id_set:        # Check for length of line and if the id is not in id_set
            id_set.add(line[0])
            clean_lines.append(line_og)
            clean_count += 1
        else:
            bad_count += 1
    print 'Good:',clean_count,'Bad:',bad_count,'Total:',line_count
    print len(clean_lines)


# ### Step n : Write stuff to file

# In[21]:

with open(basepath+outputFile,'a+') as f:
    print 'Writing stuff to the file'
    for line in clean_lines:
        f.write(line)
    f.write('\n')
print 'Added',len(clean_lines),'lines to the file'

