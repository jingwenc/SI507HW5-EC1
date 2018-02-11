from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time:
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username=sys.argv[1]
num_tweets=sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching


CACHE_FNAME = 'cache_file_name.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
        alphabetized_keys = sorted(params.keys())
        res = []
        for k in alphabetized_keys:
            res.append("{}={}".format(k, params[k]))
        return baseurl +"?"+ "&".join(res)

def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION:
        print("Fetching cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        response=requests.get(baseurl,params,auth=auth)
        CACHE_DICTION[unique_ident] = json.loads(response.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

#Finish parts 1 and 2 and then come back to this

#Code for Part 1:Get Tweets
def get_tweets(username,num_tweets):
    baseurl='https://api.twitter.com/1.1/statuses/user_timeline.json'
    d={'screen_name':username,'count':num_tweets}
    response=make_request_using_cache(baseurl, params=d)
    tweet=open('tweet.json','w')
    tweet_script=json.dumps(response,indent=2)
    tweet_content=tweet.write(tweet_script)
    tweet.close()
    return(response)


# Code for Part 2:Analyze Tweets
def frequency_of_words(username,num_tweets):
    response=get_tweets(username,num_tweets)
    text_list=[]
    for i in response:
        text=i["text"]
        text_content=nltk.word_tokenize(text)
        text_list+=text_content
    text_word=[]
    for j in text_list:
        if j.isalpha() and j!="RT" and j!="http" and j!="https":
            text_word.append(j)
    frequency=nltk.FreqDist(text_word)
    return frequency.items()

def top_five(list_original):
    list_new=[]
    for i in list_original:
        list_new.append((i[1],i[0]))
    list_new=sorted(list_new)
    return list_new[-5:]

frequency=frequency_of_words(username,num_tweets)
top_word_list=[]
top_word_list=top_five(frequency)
words=''
for word in top_word_list:
    words =' '*2+word[1]+'('+str(word[0])+')'+words

if __name__ == "__main__":
    print('USER:',username)
    print('TWEETS ANALYZED:',num_tweets)
    print('5 MOST FREQUENT WORDS:',words)


if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
