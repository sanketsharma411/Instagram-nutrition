############# Loading the negative words
with open('excluded_fooditems.txt','r') as f:
    lines = f.readlines()
excluded_tags= set()

for line in lines:
    excluded_tags.add(line.strip())
############## Loading the Post file
filename = 'sample_post.txt'
with open(filename, 'r') as f:
    lines = f.readlines()
with open(filename+'clean.txt','a+') as f:
    for line in lines:
        if line.split('\t')[7] not in excluded_tags:
            f.write(line)
    