
# coding: utf-8

# In[ ]:


import requests_oauthlib
import json
import string
import csv

client_key = ''
client_secret = ''

if not client_secret or not client_key:
    print("You need to fill in client_key and client_secret. See comments in the code around line 8-14.")


# In[ ]:


def get_tokens():
    oauth = requests_oauthlib.OAuth1Session(client_key, client_secret=client_secret)

    request_token_url = 'https://api.twitter.com/oauth/request_token'

    fetch_response = oauth.fetch_request_token(request_token_url)

    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    
    authorization_url = oauth.authorization_url(base_authorization_url)

    print("""Please click on the URL below, 
          click on "Authorize App", 
          and then copy the authorization code and paste it below.""")
    print(authorization_url)
    
    verifier = input('Please input the verifier>>> ')

    oauth = requests_oauthlib.OAuth1Session(client_key,
                              client_secret=client_secret,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret,
                              verifier=verifier)

    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    return (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier)


# In[ ]:


try:
    f = open("creds.txt", 'r')
    (client_key, client_secret, resource_owner_key, resource_owner_secret,
     verifier) = json.loads(f.read())
    f.close()
except:
    tokens = get_tokens()
    f = open("creds.txt", 'w')
    f.write(json.dumps(tokens))
    f.close()
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = tokens


# In[ ]:


protected_url = 'https://api.twitter.com/1.1/account/settings.json'
oauth = requests_oauthlib.OAuth1Session(client_key,
                        client_secret=client_secret,
                        resource_owner_key=resource_owner_key,
                        resource_owner_secret=resource_owner_secret)


# In[ ]:


response = oauth.get("https://api.twitter.com/1.1/search/tweets.json", 
              params = {'q': input('Enter a hashtag: '), 'count' : 200}) 

print(response)


# In[ ]:


content = response.json()

tweet_dictionaries = content['statuses']


# In[ ]:


class Tweet():
    def __init__(self, tweets_d = {}):
        
        self.screen_name = tweets_d['user']['screen_name']
        
        self.message = tweets_d['text']
    
    def removing_stop_words(self):
        
        no_stop_words= []
        
        stopwords = ["https://","ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out", "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such", "into", "of", "most", "itself", "other", "off", "is", "s", "am", "or", "who", "as", "from", "him", "each", "the", "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "don", "nor", "me", "were", "her", "more", "himself", "this", "down", "should", "our", "their", "while", "above", "both", "up", "to", "ours", "had", "she", "all", "no", "when", "at", "any", "before", "them", "same", "and", "been", "have", "in", "will", "on", "does", "yourselves", "then", "that", "because", "what", "over", "why", "so", "can", "did", "not", "now", "under", "he", "you", "herself", "has", "just", "where", "too", "only", "myself", "which", "those", "i", "after", "few", "whom", "t", "being", "if", "theirs", "my", "against", "a", "by", "doing", "it", "how", "further", "was", "here", "than", "it’s", "It’s", "RT", "The"]
        letters = list(string.ascii_letters)
        twitter_specific = ["@", "#","."]
        
        for x in self.message.split():
            if x not in stopwords and x not in letters and x[0] not in twitter_specific:
                no_stop_words.append(x)
        
        return no_stop_words

            
    def __str__(self,  tweets_d = {}):
        return "User @{} Tweeted: {}".format(self.screen_name, self.message)


# In[ ]:


tweet_instances = []

for a_tweet in tweet_dictionaries:
    post = Tweet(a_tweet)
    tweet_instances.append(post)

big_list_of_words = []

for x in tweet_instances:
    big_list_of_words.append(x.removing_stop_words())
    

final_list_of_words= []

for x in big_list_of_words:
    for new_list in x:
        final_list_of_words.append(new_list)
        
final_list_of_words


# In[ ]:


tweetwordcount = {}

for word in final_list_of_words:
    if word in tweetwordcount:
        tweetwordcount[word] += 1
    else:
        tweetwordcount[word] = 1


sort_filtered_tweetwordcount = sorted(tweetwordcount.items(), key=lambda x: x[1], reverse = True)
mostcommonword = sort_filtered_tweetwordcount[0][0]

print(mostcommonword)


# In[ ]:


def get_itunes(x):

    itunes_response = oauth.get("https://itunes.apple.com/search?parameterkeyvalue", 
              params = {'term': x, 'media' : 'music', 'durationInMillis': 'durationInMillis'})
    return itunes_response


# In[ ]:


itunes_response = get_itunes(mostcommonword)

itunes_content = itunes_response.json()

itunes_dictionaries = itunes_content['results']

print(itunes_dictionaries)


# In[ ]:


class Song():
    def __init__(self, itunes_d = {}):
        
        self.title = itunes_d['trackName']
        
        self.artist = itunes_d['artistName']
        
        self.length = itunes_d['trackTimeMillis']
        
        self.album = itunes_d['collectionName']
        
    def convert_to_seconds(self):
        
        return self.length / 1000
        
    def __str__(self,  itunes_d = {}):
        return "{}, by {}, is  {} miliseconds long.".format(self.title, self.artist, self.length)


# In[ ]:


for a_song in itunes_dictionaries:
    song = Song(a_song)
    print(song.title)
    print(song.artist)
    print(song.album)
    print(song.length)
    print('--------')


# In[ ]:


songlengthlist = []

for a_song in itunes_dictionaries:
    music = Song(a_song)
    songlengthlist.append(a_song)

sorted_songlengthlist = sorted(songlengthlist, key=lambda x: x['trackTimeMillis'], reverse = True)


sortedsonginstances = []

for x in sorted_songlengthlist:
    music = Song(x)
    sortedsonginstances.append(music)


# In[ ]:


f = open("songs.csv", "w")
f.write("Song Title, Artist, Length, Album\n")

for song in sortedsonginstances:
    f.write('{},{},{},{}\n'.format(song.title,song.artist,song.convert_to_seconds(),song.album))

f.close()

