""" Script that selects and shreds Reddit posts and comments. This script
DOES NOT DISCRIMINATE it will overwrite your entire post and comment history
with no exceptions.

Make yourself an Reddit app (google it) and input your info in the praw.Reddit
object below. 

Written by Josh Harkema -- josh@joshharkema.com
"""

import praw
import random
import string

def stringGenerator(size=36, chars=string.ascii_letters + string.digits):
    """ Returns a random string of numbers and letters. """
    return "".join(random.choice(chars) for _ in range(size))

reddit = praw.Reddit(client_id = '',
					 client_secret = '',
					 password = '',
					 user_agent = 'testscript by /u/X_X_X',
					 username = '')

for comment in reddit.user.me().comments.new(limit=None):
	comment.edit(stringGenerator())
	comment.delete()

for submission in reddit.user.me().submissions.new(limit=None):
	submission.delete()
