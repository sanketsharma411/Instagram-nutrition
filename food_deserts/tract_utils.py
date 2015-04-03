
def tract2line(tract,tract_dict, missing = False):
    # It will follow the following format
    FORMAT = ['tract_id','avg_cal','avg_sug','avg_fat','avg_cho','avg_fib','avg_pro','num_posts','avg_posts',\
          'fd','State','POP2010','Rural','LowIncomeTracts','UATYP10','centroid']
    st = tract
    if not missing:
        for col in FORMAT[1:]:st += '\t'+str(tract_dict[col]) 
    else:
        for col in FORMAT[1:]: st += '\t'+str(tract_dict[col]) if col in tract_dict else '\tNone'
    return st
#========================================================================================================#
def line2tract(line):
    # Loads one line and returns a dict of tract:{tract_info}
    # With the info converted into the specific format [float mostly, or bool]
    line = line.strip().split('\t')
    tract_vals = {}
    i = 0
    tract = line[i];i += 1
    tract_vals['avg_cal'] = float(line[i]);i += 1
    tract_vals['avg_sug'] = float(line[i]);i += 1
    tract_vals['avg_fat'] = float(line[i]);i += 1
    tract_vals['avg_cho'] = float(line[i]);i += 1
    tract_vals['avg_fib'] = float(line[i]);i += 1
    tract_vals['avg_pro'] = float(line[i]);i += 1
    tract_vals['num_posts'] = int(line[i]);i += 1
    tract_vals['avg_posts'] = float(line[i]);i += 1
    tract_vals['fd'] = bool(int(line[i]));i += 1
    tract_vals['State'] = line[i];i += 1
    tract_vals['POP2010'] = int(line[i]);i += 1
    tract_vals['Rural'] = bool(int(line[i]));i += 1
    tract_vals['LowIncomeTracts'] = bool(int(line[i]));i += 1
    tract_vals['UATYP10'] = line[i];i += 1
    tract_vals['centroid'] = [float(val) for val in line[i][1:-1].split(',')];i += 1
    
    return {tract:tract_vals}
	
#========================================================================================================#

def get_variable_lookup_dict(filename):
    variable_lookup_dict = {}
    with open(filename,'r') as f:
        lines = f.readlines()
    for i in range(2,65):
        name = lines[i].strip().split(',')[0]
        desc = ','.join(lines[i].strip().split(',')[1:])
        variable_lookup_dict[name] = desc
    return variable_lookup_dict

#========================================================================================================#

def getTractInfo(filename):
    with open(filename,'r') as f:
        lines = f.readlines()
    # Getting the list of descriptors
    desc_keys = lines[0].strip().split(',')
    tract_info = {}
    # Now making the dict
    for line in lines[1:]:
        line = line.strip().split(',')
        tract_id = '0'+ line[0] if len(line[0]) == 10 else line[0]
        tract_info[tract_id] = {}
        for i in range(1,len(desc_keys)):
            tract_info[tract_id].update({desc_keys[i]:line[i]})
    return tract_info
#========================================================================================================#
with open('C:\Users\Shweta\Desktop\CS 8903\FINAL/food_deserts\data/food_deserts_ids.txt','r') as f:
    lines = f.readlines()
lines = set([line.strip() for line in lines])
def isFD(tract):
	# 'return tract in lines'  also works
    if tract in lines: return True
    else: return False

def loadTractFile(filename):
	'''
	Uses the line2tract function to return a tractDict of all the entries
	'''
	# Loading the file in 
	with open(filename,'r') as f:
		lines = f.readlines()
	tractDict = {}
	for line in lines:
		tractDict.update(line2tract(line))
	return tractDict