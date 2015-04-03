
# coding: utf-8

# ### See readme.txt

# In[1]:

from datetime import datetime


# In[2]:

# Interim Status file
f_interim_status = open('join_Interim_Status.txt','w+')
#basepath = 'C:/Users/Shweta/Desktop/CS 8903/FINAL/split/test/join nut to loc//'

basepath = '/nethome/ssharma321/split_data_2/split_data//'

for i in range(0,1):
    US_filename = basepath+str(i)+'//post.txt.US'
    nut_filename = basepath+str(i)+'//post.txt.nut'
    #####################################################################################################
    ''' Opening the right files and loading the data'''
    #####################################################################################################
    print i,'loading US file'
    f_interim_status.write(str(datetime.now())+'\t'+str(i)+' loading US file'+'\n')
    with open(US_filename,'r') as f:
        US_lines = f.readlines()
    US_dict = {}
    for line in US_lines:
        US_dict[line.split('\t')[0]] = line.strip() 
    print i,'loading US file !! DONE !!'
    f_interim_status.write(str(datetime.now())+'\t'+str(i)+' loading US file !! DONE !!'+'\n')

    print i,'loading nut file'
    f_interim_status.write(str(datetime.now())+'\t'+str(i)+' loading nut file'+'\n')
    nut_dict = {}
    with open(nut_filename,'r') as f:
        nut_lines = f.readlines()
    for line in nut_lines:
        nut_dict[line.split('\t')[0]] = line.strip() 
    print i,'loading nut file !! DONE !!'
    f_interim_status.write(str(datetime.now())+'\t'+str(i)+' loading nut file !! DONE !!'+'\n')
    #####################################################################################################
    ''' Setting output stuff up '''
    #####################################################################################################
    print i,'Setting nut.US file'
    f_interim_status.write(str(datetime.now())+'\t'+str(i)+' Setting nut.US file'+'\n')
    f_output = open(basepath+str(i)+'//post.txt.nut.US','w+')

    #####################################################################################################
    ''' The Process '''
    #####################################################################################################
    count = 0
    st = ''
    for line in US_lines:
        line =  line.strip().split('\t')
        post_id = line[0]
        start = '\t'.join(line[0:16])
        end = '\t'.join(line[16:])
        mid = '\t'.join(nut_dict[post_id].split('\t')[2:])

        count += 1
        st += start+'\t'+mid+'\t'+end+'\n'
        if not count%10000:
            print count
            f_interim_status.write(str(datetime.now())+'\t'+str(i)+' '+str(count)+'\n')
            f_output.write(st)
            st = ''

    # Writing any leftovers    
    f_output.write(st)

    #####################################################################################################
    '''Finishing stuff up '''
    #####################################################################################################
    f_output.close()
    print 'Completed'
    f_interim_status.write(str(datetime.now())+'\t'+str(i)+                           ' ================================Completed======================================'+'\n')

f_interim_status.close()

