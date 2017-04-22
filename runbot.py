import praw
import sys
from winsound import Beep

#function to check percentage match
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

#function to log activity to avoid duplicate comments
def log(ID):
    with open('actions.txt', 'a+') as ActRecord:
        ActRecord.write('\n' + str(ID))

#function to increment and output number of posts scanned so far
def progress():
    global Scanned
    Scanned += 1
    if Scanned % 100 == 0:
        print(str(Scanned) + ' posts scanned')
        Beep(125, 250)

#details
BotA = {'ClientID': 'FmFQgtKl41ehaQ',
        'ClientSecret': 'l9PvV_Pr10la_YsCWQN6PPXH_C0',
        'UserAgent': 'python3.6.1:darthplagueisbot:v1 (by /u/Sgp15)',
        'Username': 'darthplagueisbot',
        'Password': 'CoreHairSee62'}

Account = BotA

#initialise reddit object with details
reddit = praw.Reddit(client_id = Account['ClientID'],
                     client_secret = Account['ClientSecret'],
                     password = Account['Password'],
                     user_agent = Account['UserAgent'],
                     username = Account['Username'])

subreddit = reddit.subreddit('test')

Tragedy = 'I thought not. It\'s not a story the Jedi would tell you. It\'s a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life... He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful... the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. It\'s ironic he could save others from death, but not himself.'

#run bot
Scanned = 0
ActRecord = open('actions.txt', 'r')
Record = ActRecord.read()
while True:
    for submission in subreddit.stream.submissions():
        try:
            progress()
            if findt(submission.title, 1) and not str(submission) in Record:
                Beep(250, 250)
                print('')
                print(submission.title)
                print(submission.author)
                print(findt(submission.title, 0))
                submission.reply(Tragedy)
                log(submission)
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                progress()
                if findt(comment.body, 1) and not str(comment) in Record:
                    Beep(250, 250)
                    print('')
                    print(comment.body)
                    print(comment.author)
                    print(findt(comment.body, 0))
                    comment.reply(Tragedy)
                    log(comment)
        except:
            print('ERROR')
            e = sys.exc_info()
            print(e)
            
