""" Application to select and shred Reddit posts and comments. Set how much
of your history you'd like to preserve with the MAXIMUM_AGE constant below.

Written by Josh Harkema -- josh@joshharkema.com
"""

import datetime
import random
import string
import praw


MAXIMUM_AGE = 24  # in hours

def delta_now():
    """ Returns now + MAXIMUM_AGE for the comparison."""
    delta = datetime.datetime.now() + datetime.timedelta(hours=MAXIMUM_AGE)
    return delta

def string_generator(size=36, chars=string.ascii_letters + string.digits):
    """ Returns a random string of numbers and letters."""
    return "".join(random.choice(chars) for _ in range(size))

def main():
    """ The reddit object, everything is case sensitive."""
    reddit = praw.Reddit(client_id='',
                         client_secret='',
                         password='',
                         user_agent='testscript by /u/X_X_X',
                         username='')

    # calls comments and submissions as iterable objects
    my_comments = reddit.user.me().comments.new(limit=None)
    my_submissions = reddit.user.me().submissions.new(limit=None)

    for comment in my_comments:
        # time object, pretty self explanatory
        time = datetime.datetime.fromtimestamp(comment.created)

        # this overwrites the comment, saves it and deletes it
        if time > delta_now():
            comment.edit(string_generator())
            comment.delete()
            print(comment, "deleted")
        else:
            print(comment, "skipped")

    # Iterates through submissions and nukes them, there is no way to overwrite
    # them like the comments
    for submission in my_submissions:
        # same story as the comments loop above, sans editing
        time = datetime.datetime.fromtimestamp(submission.created)

        # delete the submssion
        if time > delta_now():
            submission.delete()
            print(submission, "deleted")
        else:
            print(submission, "skipped")

    print("Your Reddit account has been shredded successfully.")

main()
