file_name = 'C:\Users\Shweta\Desktop\CS 8903\FINAL\Data\\sample_comments.txt'
with open(file_name,'r') as f:
    lines = f.readlines()
lines = list(set(lines))
with open(file_name+'du.txt','w+') as f:
    for line in lines:
        f.write(line)
