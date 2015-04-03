Call the function 
	post, comments, likes, users_tagged, users =  parse_post(one_post_json, some_string)
	with the following arguments:
		one_post_json : JSON object for one post
		some_string :  I used this to print the seed tag,you may pass any string [make sure it does not have a tab in it].
This function returns a tuple of strings
I did write each string to a separate file, so there were 5 files corresponding to each of these strings.
		
post:
- Each line is a post
- Each line has the following fields
	id
	user_has_liked
	type : video/image
	filter 
	created_time [UTC_timestamp]
	link : instagram link for the post
	OP user_id 
	some_string : This is the second argument passed to the function parse_post(). it is printed same as it was passed.
	tags : comma separated tags
	image_url : link to the image/video file, so this gives the .jpg or .mp4 file
	caption_id : = 'NA' if no id exists
	caption_text : = 'NA' if no caption exists
	Location : Comma separated 
		lat, lon, location_name, location_id
		for any field which does not exist it is NA
	num_comments
	num_likes
	num_users_in_photo
	
comments:
- Each line is a comment
- One post might have multiple comments, this file has a line for each comment, so one post_id might appear multiple times in this file
- Each line has the following fields
	post_id
	comment_id
	timestamp
	text
	user_id

likes:
- Each line corresponds to a the likes related to a single post, so one post_id should appear only once in this file
- So the only field associated with a like is the number of likes, and the user_ids of those who have liked it
- Each line has the following fields
	post_id
	num_likes
	users_who_liked_it : comma separated user ids [has a trailing comma, you might wanna use likes.strip(',')]

users_tagged:
- Each line corresponds to a user being tagged in the image 
- Each line has the following fields
- Multiple users can be tagged in the same image, so one post_id might appear multiple time in this file
	post_id
	x position
	y position
	user id

users:
- Each line corresponds to the mention of a user
- One post might have multiple mentioned users, so this string might have multiple lines for each post
- So if a user is tagged in the image, has commented and liked the image, then this file will have 3 lines for the user, with every field same except for the last one which would be COMMENT, LIKE, TAG for the 3 distinct lines.
- something like this
	1584087370	dany_rrpp	Lista Joy - OchoYMedio - Pacha	https://scontent-b.cdninstagram.com/hphotos-xpa1/l/t51.2885-19/928618_277356505722137_448347779_a.jpg	NA	NA	918660769475005704_1584087370	COMMENT
	1584087370	dany_rrpp	Lista Joy - OchoYMedio - Pacha	https://scontent-b.cdninstagram.com/hphotos-xpa1/l/t51.2885-19/928618_277356505722137_448347779_a.jpg	NA	NA	918660769475005704_1584087370	LIKE
	1584087370	dany_rrpp	Lista Joy - OchoYMedio - Pacha	https://scontent-b.cdninstagram.com/hphotos-xpa1/l/t51.2885-19/928618_277356505722137_448347779_a.jpg	NA	NA	918660769475005704_1584087370	TAG
- Each line has the following fields
	user_id
	username
	full_name
	profile picture 
	bio : = 'NA' if non exsitent
	website: = 'NA' if non existent
	associated post_id
	association type: POST or LIKE or COMMENT or TAG
