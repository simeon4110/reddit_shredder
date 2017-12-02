""" Application to select and shred Reddit posts and comments. Set how much
of your history you'd like to preserve with the MAXIMUM_AGE constant below.

Written by Josh Harkema -- josh@joshharkema.com
"""

import datetime
import random
import string

import praw

############################
#   Enter Your Info Here   #
############################
MAXIMUM_AGE = 24  # in hours
CLIENT_ID =
CLIENT_SECRET =
PASSWORD =
USERNAME =


def delta_now():
    """
    Creates a time object for the comment/post timestamp minus
    MAXIMUM_AGE.

    :return: A time object.
    """
    delta = datetime.datetime.utcnow() - datetime.timedelta(hours=MAXIMUM_AGE)
    return delta

def string_generator(size=36, chars=string.ascii_letters + string.digits):
    """
    Returns a random string of numbers and letters.

    :param size: The length of the string.
    :param chars: They type of characters.
    :return: A string of random characters.
    """
    return "".join(random.choice(chars) for _ in range(size))

def main():
    """
    The actual shredder script. Connects to the Reddit API with PRAW.

    :return: Nothing, prints directly to the console.
    """
    user_agent = str("test script by u/%s" % USERNAME)
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         password=PASSWORD,
                         user_agent=user_agent,
                         username=USERNAME)

    # calls comments and submissions as iterable objects
    my_comments = reddit.user.me().comments.new(limit=None)
    my_submissions = reddit.user.me().submissions.new(limit=None)

    for comment in my_comments:
        time = datetime.datetime.fromtimestamp(comment.created)
        # this overwrites the comment, saves it and deletes it
        if time < delta_now():
            comment.edit(string_generator())
            comment.delete()
            print("Comment:", comment, "Overwriten with: '%s' DELETED"
			               % comment.body)
        else:
            print("Comment:", comment, "Body: '%s' SKIPPED"
			               % comment.body)

    # Iterates through submissions and nukes them, there is no way to
    # overwrite them like the comments
    for submission in my_submissions:
        time = datetime.datetime.fromtimestamp(submission.created)
        # delete the submssion
        if time < delta_now():
            submission.delete()
            print("Submission:", submission, "Titled: '%s' DELETED"
			               % submission.title)
        else:
            print("Submission:", submission, "Titled: '%s' SKIPPED"
			               % submission.title)

    print("At, %s, your Reddit account was shredded successfully."
	         % datetime.datetime.now())

main()
