import os,sys
sys.path.append('/nethome/ssharma321/FINAL/scripts')
from InstaLib import setup_api ,get_info_tags, clean_text, parse_user, parse_post, get_posts_to_file
import json,re, pickle
#############################################################################
import urllib2, pickle
from bs4 import BeautifulSoup

tag_set = set()
tag_file = 'seed_tags_7Feb.txt'
with open(tag_file,'r') as f:
    lines = f.readlines()

for line in lines:
    tag_set.add(str(line.strip().lower()))

tag_set = list(tag_set)
#############################################################################
ACCESS_TOKEN = setup_api()      
get_posts_to_file(tag_set,6000,ACCESS_TOKEN,sleep = 0.75)
