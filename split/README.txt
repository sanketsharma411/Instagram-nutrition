This folder contains scripts to split the big post.txt file obtained from the crawl into multiple smaller files. If you are running this on a server, splitting up data this way would make processing multiple [how many ?] times faster.

So here are the steps:
1) Complete the crawl, and get the post.txt file
2) Split it up using
		split_post.py
			Specify the base path and number of splits
3) For each of the split files
	i. Get nut info using 
		post2nut_for_server.py  [MULTI ALERT ! READ NOTE BELOW]
		So in this file change the 
			basepath
	
	ii. Get loc info using	
		post2loc_US.py			[MULTI ALERT ! READ NOTE BELOW]
	
	iii.Combine these two using 
		join_nut_loc.py
		Modify the following
			basepath
			start,end

4) Combine all the location files
		combine_split_nut_loc.py
		basepath
		start,end
	
NOTE:You will first have to create multiple copies of (3.i) and (3.ii) file and setup multiple cronjobs to run the stuff in parallel
	Make any required changes to
		create_copies.py
	