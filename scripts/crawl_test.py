import sys
from script import *
from InstaLib import setup_api
query = "https://api.instagram.com/v1/tags/"
tag = 'madrid'
request = "/media/recent?access_token="
url = query+tag+request+setup_api()
response = urllib2.urlopen(url)
data = json.load(response)
inst = data['data'][0]
s,c,l,u_in_photo,user = parse_post(inst,tag)
