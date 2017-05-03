import praw
import sys
from time import sleep
from os import environ
import bmemcached
from difflib import SequenceMatcher

#function to check percentage match
def findmatch(Text, Object, PercForMatch, WhichData):
    Text = Text.lower()
    Object = Object.lower()
    
    OWords = Object.split()
    
    PercPerWord = (1 / float(len(OWords))) * 100

    MatchPerc = 0
    for i in range(len(OWords)):
        if OWords[i] in Text:
            MatchPerc += PercPerWord

    if MatchPerc >= PercForMatch:
        Match = True
    else:
        Match = False

    if WhichData == 1:
        return Match
    else:
        return MatchPerc

#function to search for the phrase
def findt(Text, Type):
    Tragedy = 'Did you ever hear the tragedy of Darth Plagueis the wise'
    return findmatch(Text, Tragedy, 73, Type)

#function to search for specific words using difflib
def wordmatch(Text, Object):
    #split string into individual words
    TWords = Text.split()
    #check each word
    for i in range(len(TWords)):
        #if word is more than 80% match, return 'True'
        if SequenceMatcher(None, Object, TWords[i]).ratio() > 0.8:
            return True

#initialise cache using details in premade environmental variable
Cache = bmemcached.Client(environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
                          environ.get('MEMCACHEDCLOUD_USERNAME'),
                          environ.get('MEMCACHEDCLOUD_PASSWORD'))

#function to log activity to avoid duplicate comments
def log(ID):
    #add id to log
    Cache.set('actions', Cache.get('actions') + [str(ID)])
    #add 1 to 'Matches'
    Cache.set('Matches', Cache.get('Matches') + 1)

#function to increment, output and log number of posts scanned so far
Scanned = Cache.get('Scanned')
def progress():
    global Scanned
    #add 1 to 'Scanned'
    Scanned += 1
    #if 'Scanned' is a multiple of 10, dislay it and record it to cache
    if Scanned % 10 == 0:
        print(str(Scanned) + ' comments scanned.')
        Cache.set('Scanned', Scanned)

#fetch details from environmental variables
BotA = {'ClientID': environ['ClientID'],
        'ClientSecret': environ['ClientSecret'],
        'Password': environ['Password'],
        'UserAgent': 'python3.6.1:darthplagueisbot:v1.3.3 (by /u/Sgp15)',
        'Username': environ['Username']}

#initialise reddit object with details
reddit = praw.Reddit(client_id = BotA['ClientID'],
                     client_secret = BotA['ClientSecret'],
                     password = BotA['Password'],
                     user_agent = BotA['UserAgent'],
                     username = BotA['Username'])

#which subreddit bot will be active in
subreddit = reddit.subreddit('PrequelMemes')

#phrase to reply with
Tragedy = 'I thought not. It\'s not a story the Jedi would tell you. It\'s a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life... He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful... the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. It\'s ironic he could save others from death, but not himself.'

#run bot
while True:
    #start reading comment stream
    for comment in subreddit.stream.comments():
        try:
            progress()
            #check for general match
            if findt(comment.body, 1)
            #check for essential terms
            and wordmatch(str(comment.body).lower(), 'plagueis')
            and wordmatch(str(comment.body).lower(), 'tragedy')
            #check comment has not been replied to alread
            and not str(comment) in Cache.get('actions')
            #check comment is not the wrong phrase
            and not findmatch(comment.body, Tragedy, 66, 1):
                #newline
                print('')
                #display id, body, author and match percentage of comment
                print(comment)
                print(comment.body)
                print(comment.author)
                print(findt(comment.body, 0))
                #reply to comment
                comment.reply(Tragedy)
                #add comment to list of comments that have been replied to
                log(comment)
                #newline
                print('')
        #countdown for new accounts with limited comments/minute
        except praw.exceptions.APIException as err:
            ErrorDetails = str(err)
            #get time till you can comment again from error details
            WaitTime = ErrorDetails[54:55]
            print('Wait ' + WaitTime + ' minutes to work.')
            Time = int(WaitTime)
            #display time remaining every minute
            for i in range(Time):
                sleep(60)
                Time -= 1
                print(str(Time) + ' minute(s) left.')
        #generic error handler
        except:
            print('ERROR')
            #get error details and display them
            e = sys.exc_info()
            print(e)
            
