import os
#os.chdir('C:\Users\Shweta\Desktop\CS 8903\FINAL\\food_list\Direct Names vs Added Names')

#############################################################333
direct_website_names = set()
with open('direct_website_names.txt','r') as f:
    lines  = f.readlines()
for line in lines:
    direct_website_names.add(line.strip().lower())
print direct_website_names
         

#############################################################333
added_names = set()
lines  = []
with open('Big_from_server.txt','r') as f:
    lines  = f.readlines()
for line in lines:
    added_names.add(line.strip().lower())
print len(added_names)

###################################################################
# From website : 574 [filename : direct_Website_names.txt]
# Removed : dry, ate, cupboard, system, pop, blackeyed, hot,
#           main, order, digest
# Added : hashbrown, groceries, delicious, breakfast, snack, yummy,
#         cooking, instafood, icecream, pizza, nutrition, eating,
#         foodporn, vegan, lunch, croissant, fajita, feast,
#         donut, dinner, yum, tasty, meal
# Final : 588 [filename : Big_from_server.txt]
# Math  : 574 - 10 + 24 = 588

