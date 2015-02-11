file_name = 'sample_comments.txt'
with open(file_name,'r') as f:
    lines = f.readlines()
lines = list(set(lines))
with open(file_name+'du.txt','w+') as f:
    for line in lines:
        f.write(line)
