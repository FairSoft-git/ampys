import math
# Use these constants in place of int and string literals to make your code
# easier to read, and less error prone.
# Note that we are using a shorter tweet length to make testing easier.
MAX_TWEET_LENGTH = 50
HASH = '#'


# Add your own constants here, as needed


def contains_owly_url(tweet):
    """ (str) -> bool

    Return True if and only if tweet contains a link to an ow.ly URL of the 
    form 'http://ow.ly/'.

    Assume tweet is a valid tweet.

    >>> contains_owly_url('Cook receives award: http://ow.ly/WXJFN')
    True
    >>> contains_owly_url('http://ow.ly/VGpA9 Team to transform U of T campus')
    True
    >>> contains_owly_url('Fairgrieve to play in goal http://www.nhl.com')
    False
    """
    # Complete this function body.
    index = tweet.find('http://ow.ly/')
    if index != -1:
        if index == 0:
            return True
        elif tweet[index - 1] == ' ':
            return True

    return False

# Now define the other functions described in the handout.
def is_valid_tweet(tweet):
    """ (str) -> bool 

    Return True if and only if the length of the tweet is between 1 and
    MAX_TWEET_LENGTH.

    >>> is_valid_tweet('The first midterm is on Feb. 24th! LOL!')
    True
    >>> is_valid_tweet("They said this tweet will not be valid if it's length"\
    +"is greater than fifty characters. I don't think so. That's why I write"\
    +" this tweet. Is this tweet posted?")
    False
    """

    return len(tweet) <= MAX_TWEET_LENGTH and len(tweet) >= 0

def add_hashtag(valid_tweet, hashtag_text):
    """ (str, str) -> str

    Return a hashtag included tweet, i.e. valid_tweet #hashtag_text.
    if the new tweet is shorter than MAX_TWEET_LENGTH.
    Otherwise return the valid_tweet.

    Assume valid_tweet is a valid tweet.

    >>> add_hashtag('This is not cold at all for', 'Winter2016')
    'This is not cold at all for #Winter2016'
    >>> add_hashtag('This is not cold at all for', 'Canada_Toronto_Winter2016')
    'This is not cold at all for'
    """

    if len(valid_tweet + ' ' + HASH + hashtag_text) <= MAX_TWEET_LENGTH:
        return valid_tweet + ' ' + HASH + hashtag_text
    else:
        return valid_tweet

def contains_hashtag(valid_tweet, hashtag):
    """ (str, str) -> bool

    Return True if and only if the hashtag is in valid_tweet.

    Assume valid_tweet is a valid tweet.

    >>> contains_hashtag('This is not cold at all for #Winter2016', 
        '#Winter2016')
    True
    >>> contains_hashtag('The #readingweek is not far.', '#reading_week')
    False
    """
    if len(hashtag) == 0 or hashtag[0] != HASH:
        return False

    index = valid_tweet.find(hashtag)
    if index != -1:
        if index + len(hashtag) == len(valid_tweet):
            return True
        elif valid_tweet[index + len(hashtag)] == ' ':
            return True

    return False


def report_longest(tweet1, tweet2):
    """ (str, str) -> str

    Return the longer tweet from tweet1 and tweet2 or return Same length
    if they have the same length.

    Assume tweet1 and tweet2 are valid tweets.

    >>> report_longest('The first midterm is on Feb. 24th! LOL!', 'This is not'\
    + ' cold at all for #Winter2016')
    'Same length'
    >>> report_longest('I do not like cold winter.', 'This is not cold at all'\
    + ' for #Winter2016')
    'Tweet 2'
    """

    if len(tweet1) > len(tweet2):
        return 'Tweet 1'
    elif len(tweet1) < len(tweet2):
        return 'Tweet 2'
    else:
        return 'Same length'

def num_tweets_required(message):
    """ (str) -> int

    Return the minimum number of tweets that can build the whole message.

    >>> num_tweets_required('This is not cold at all for'\
    + '#Canada_Toronto_Winter2016')
    2
    >>> num_tweets_required("They said this tweet will not be valid if it's"\
    + " length is greater than fifty characters. I don't think so. That's why"\
    + " I write this tweet. Is this tweet posted?")
    4
    """
    return math.ceil(float(len(message)) / MAX_TWEET_LENGTH)

def get_nth_tweet(message, number):
    """ (str, int) -> str

    Return the nth number of tweet after splitting a message into many tweets.

    >>> get_nth_tweet("They said this tweet will not be valid if it's length"\
    + " is greater than fifty characters. I don't think so. That's why I"\
    + " write this tweet. Is this tweet posted?", 2)
    "gth is greater than fifty characters. I don't thin"
    >>> get_nth_tweet('This is not cold at all for'\
    + ' #Canada_Toronto_Winter2016', 10)
    ''
    """
    return message[(number - 1) * MAX_TWEET_LENGTH: number * MAX_TWEET_LENGTH]