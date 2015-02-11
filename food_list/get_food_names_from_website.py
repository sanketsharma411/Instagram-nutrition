# file for getting food names from http://www.enchantedlearning.com/wordlist/food.shtml
import urllib2, pickle
from bs4 import BeautifulSoup
####################

url = 'http://www.enchantedlearning.com/wordlist/food.shtml'
data = urllib2.urlopen(url).read().split('\n')

#data = data.read().split('\n')
food_names = []
# Loading it into Food Names
for line in data:
    if '<BR>' in line:
        if line.split('<')[0] != '':
            #print line.split('<')[0]
            food_names.append(line.split('<')[0])

food_name_set = set()
for food_name in food_names:
    food_name_set.add(food_name.replace(' ','').replace('-',''))
                        
# Dumping it
with open('food_name_list','w') as f:
    pickle.dump(food_names,f)
# Loading it
with open('food_name_list','r') as f:
    food_names = pickle.load(f)
# Writing it into a more human readable format
with open('food_name_list.txt','w+') as f:
    for food_name in food_name_set:
        f.write(food_name + '\n')

with open('USDA_data_pickle_x','r') as f:
    USDA = pickle.load(f)

# We want the entire word to match a complete word
for k in USDA.keys():
    USDA[k]['specs'] = set(USDA[k]['specs'].split(' '))
        

###############################################33
tag_USDA_id_dict = dict.fromkeys(food_name_set)
st = ''
for food_name in food_name_set:
    st += food_name
    tag_USDA_id_dict[food_name] = set()
    for k in USDA.keys():
        if food_name in USDA[k]['specs']:
            st +='\t'+k
            tag_USDA_id_dict[food_name].add(k)
            print  food_name+'\t'+k
    st += '\n'

with open('matches','w+') as f:
    f.write(st)
    
#######################################
f = open('something.txt','w+') 
for k in tag_USDA_id_dict:
    f.write(k+'\t'+str(tag_USDA_id_dict[k])+'\n')
    
f.close()