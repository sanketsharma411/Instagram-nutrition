start = 1
end = 39
base_file_name = 'post2loc_US.py'
## Creating the files


with open(base_file_name,'r') as f:
    code = f.read()

for i in range(start,end):
    code_new = code.replace('#\ni=0\n#','#\ni='+str(i)+'\n#')
    with open('C:/Users/Shweta/Desktop/CS 8903/FINAL/split/for_server//'+str(i)+'_'+base_file_name,'w+') as f:
        f.write(code_new)


## Cronjob commands


for i in range(start,end):
    new_file_name  = str(i)+'_'+base_file_name
    print '32 11 30 3 * python '+new_file_name
