def extract_mentions(tweet):
    ''' (str) -> list of str
    '''
    
    lst = []
    i = 0
    while i < len(tweet) and tweet.find('@', i) != -1:
        start = tweet.find('@', i)
        end = tweet.find(' ', start)
        if end != -1:
            lst.append(tweet[start + 1: end])
        else:
            lst.append(tweet[start + 1:])
        i = end
    return lst

def extract_hashtags(tweet):
    ''' (str) -> list of str
    '''
    
    lst = []
    i = 0
    while i < len(tweet) and tweet.find('#', i) != -1:
        start = tweet.find('#', i)
        end = tweet.find(' ', start)
        if end != -1:
            if tweet[start + 1: end] not in lst:
                lst.append(tweet[start + 1: end])
        else:
            if tweet[start + 1:] not in lst:
                lst.append(tweet[start + 1:])
        i = end
    return lst    

def count_words(tweet, word_dict):
    ''' (str, dict of {str: int}) -> NoneType
    '''
    lst = tweet.split()
    aim = []
    for i in range(len(lst)):
        word = ''
        if lst[i][0] != '@' and lst[i][0] != '#':
            for s in lst[i]:
                if s.isupper():
                    word += s.lower()
                elif s.isdigit() or s.islower():
                    word += s
        if word != '':
            aim.append(word)
    for w in aim:
        if w not in word_dict:
            word_dict[w] = 1
        else:
            word_dict[w] += 1
            
def common_words(word_dict, limit):
    ''' (dict of {str: int}, int) -> NoneType
    '''
    word = list(word_dict.keys())
    count = list(word_dict.values())
    while len(count) > limit + 1:
        aim = min(count)
        aim_index = count.index(aim)
        del(word_dict[word[aim_index]])
        word.pop(aim_index)
        count.pop(aim_index)
    if count.count(min(count)) != 1:
        target = min(count)
        while target in count:
            del(word_dict[word[count.index(target)]])
            word.pop(count.index(target))
            count.pop(count.index(target))
    else:
        del(word_dict[word[count.index(min(count))]])
        word.pop(count.index(min(count)))
        count.pop(count.index(min(count)))

def read_tweets(file):
    ''' (file open for reading) -> dict of {str: list of tweet tuples} 
    '''
    d = {}
    line = file.readline()
    while line != '':
        c = line[:-2]
        d[c] = []
        line = file.readline()
        while line != '' and line.strip()[-1] != ':':
            lst = line.split(',')
            date = int(lst[1])
            source = lst[3]
            favourate = int(lst[4])
            retweet = int(lst[5].strip())
            tweet = ''
            line = file.readline()
            while line != '<<<EOT\n' and line != '':
                tweet += line
                line = file.readline()
            d[c].append((c, tweet, date, source, favourate, retweet))
            line = file.readline()
    return d

def most_popular(tweet_dict, d1, d2):
    ''' (dict of {str: list of tweet tuples}, int, int) -> str 
    '''
    d = {}
    for key in tweet_dict:
        d[key] = 0
        for t in tweet_dict[key]:
            if t[2] >= d1 and t[2] <= d2:
                d[key] = d[key] + t[4] + t[5]
    l1 = list(d.keys())
    l2 = list(d.values())
    if l2.count(max(l2)) != 1:
        return 'Tie'
    else:
        return l1[l2.index(max(l2))]
    
def detect_author(tweet_dict, tweet):
    '''(dict of {str: list of tweet tuples}, str) -> str
    '''
    unique_hash = get_unique_hashtags(tweet_dict)
    hashtags = extract_hashtags(tweet)
    hashs = list(unique_hash.values())
    authors = list(unique_hash.keys())
    for i in range(hashtags):
        if hashtags[i] not in hashs:
            hashtags.pop(i)
    if len(hashtags) == 1:
        return authors[hashs.index(hashtags[0])]
    else:
        return 'Unknown.'
    
#### helper ####
def get_unique_hashtags(tweet_dict):
    ''' (dict of {str: list of tweet tuples}, int, int) -> 
    dict of {str: list of str}
    '''
    d = {}
    for key in tweet_dict:
        d[key] = []
        for t in tweet_dict[key]:
            d[key].extend(extract_hashtags(t[1]))
    l2 = list(d.values())
    l3 = []
    l4 = []
    for sub in l2:
        l3.extend(sub)
    for tag in l3:
        if l3.count(tag) != 1 and (tag not in l4):
            l4.append(tag)
    for k in d:
        for i in range(d[k]):
            if d[k][i] in l4:
                d[k].pop(i)
    return d