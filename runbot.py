def findmatch(Text, Object, PercForMatch, WhichData):
    Text = Text.lower()
    Object = Object.lower()
    
    OWords = Object.split()
    
    PercPerWord = (1 / len(OWords)) * 100

    MatchPerc = 0
    for i in range(len(OWords)):
        if OWords[i] in Text:
            MatchPerc += PercPerWord
    #print(MatchPerc)

    if MatchPerc >= PercForMatch:
        Match = True
    else:
        Match = False

    if WhichData == 1:
        return Match
    else:
        return MatchPerc

def findt(Text, Type):
    Tragedy = 'Did you ever hear the tragedy of Darth Plagueis "the wise"?'
    return findmatch(Text, Tragedy, 50, Type)

#Test
ClientID = 'nope'
ClientSecret = 'nope'

import praw

UserAgent = 'python3.6.1:darthplagueisbot:v1 (by /u/Sgp15)'
Username = 'darthplagueisbot'
Password = 'doyoutakemeforafool?iamnotthatstupid'

reddit = praw.Reddit(client_id = ClientID,
                     client_secret = ClientSecret,
                     password = Password,
                     user_agent = UserAgent,
                     username = Username)

subreddit = reddit.subreddit('test')

Tragedy = 'I thought not. It\'s not a story the Jedi would tell you. It\'s a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life... He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful... the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. It\'s ironic he could save others from death, but not himself.'

import sys

while True:
    for submission in subreddit.stream.submissions():
        try:
            if findt(submission.title, 1):
                print('')
                print(submission.title)
                print(submission.author)
                print(findt(submission.title, 0))
                submission.reply(Tragedy)
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                if findt(comment.body, 1):
                    print('')
                    print(comment.body)
                    print(comment.author)
                    print(findt(comment.body, 0))
                    comment.reply(Tragedy)
        except:
            print('ERROR')
            e = sys.exc_info()
            print(e)
            
