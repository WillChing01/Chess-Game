import requests
import json
import ndjson
import ast
from requests.auth import AuthBase
import sys
import os
import math
sys.path.insert(0,os.getcwd())

from board import *

class TokenAuth(AuthBase):

    def __init__(self,token):
        self.token=token

    def __call__(self,r):
        r.headers['Authorization']=f'{self.token}'
        return r

#oauth2="Bearer G4eVqvMKHb2OJzZL"
oauth2="Bearer dA72wp8JFMerxPXo"

url_email="https://lichess.org/api/account/email"
url_getevents="https://lichess.org/api/stream/event"
url_challenge="https://lichess.org/api/challenge/"
url_game="https://lichess.org/api/bot/game/"

token=TokenAuth(oauth2)

gameon=False
gameID=""
bot_id="big_chingus_01"

def get_challenges(url):
    """check for incoming challenges, accept the first one and play"""
    global gameon, gameID
    s=requests.Session()
    challenge_accepted=False
    print("Receiving incoming challenges...")

    with s.get(url,auth=token,stream=True) as response:
        for line in response.iter_lines():
            if line:
                a=str(line.decode('utf-8'))
                a=a.replace('null','None')
                a=a.replace('true','True')
                a=a.replace('false','False')
                msg=ast.literal_eval(a)

                if msg['type']=='gameStart':
                    #start of the game.
                    gameID=msg['game']['id']
                    gameon=True
                    return None
                elif msg['type']=='gameFinish':
                    #end of the game.
                    pass
                elif msg['type']=='challenge' and challenge_accepted==False:
                    #received a new challenge.
                    #accept if not about to play a new game.
                    if msg['challenge']['variant']['key']!="standard":
                        r=requests.post(url_challenge+msg['challenge']['id']+"/decline",auth=token)
                    elif msg['challenge']['speed']!="blitz" and msg['challenge']['speed']!="rapid":
                        r=requests.post(url_challenge+msg['challenge']['id']+"/decline",auth=token)
                    else:
                        r=requests.post(url_challenge+msg['challenge']['id']+"/accept",auth=token)
                        if r.status_code==200:
                            challenge_accepted=True
                            if msg['challenge']['challenger']['title']==None:
                                print("Challenge accepted from", msg['challenge']['challenger']['id'], "of rating", msg['challenge']['challenger']['rating'],"!")
                            else:
                                print("Challenge accepted from", msg['challenge']['challenger']['title'], msg['challenge']['challenger']['id'], "of rating", msg['challenge']['challenger']['rating'],"!")
                            print("Speed:", msg['challenge']['speed'])
                            print("Time control:", msg['challenge']['timeControl']['type'])
                elif msg['type']=='challengeCanceled':
                    #cancelled the challenge.
                    pass
                elif msg['type']=='challengeDeclined':
                    #outgoing challenge was declined.
                    pass

def game_stream(ID):
    """play a game of specified ID"""
    s=requests.Session()
    print("Playing game with ID:",ID)

    #say hello.
    response=requests.post(url_game+ID+"/chat",auth=token,data={'room':'player','text':'Good luck, human.'})
    b=Board(verbose=False)
    depth=3
    lets=['a','b','c','d','e','f','g','h']
    pieces=['','r','n','b','q']
    side=0

    with s.get(url_game+"stream/"+ID,auth=token,stream=True) as response:
        for line in response.iter_lines():
            if line:
                a=str(line.decode('utf-8'))
                a=a.replace('null','None')
                a=a.replace('true','True')
                a=a.replace('false','False')
                msg=ast.literal_eval(a)
                print(msg)

                if msg['type']=='gameFull':
                    #shown at start of game. check if white and if so, play
                    if msg['white']['id']==bot_id:
                        #play the first move.
                        side=0
                        m=b.pcmove(depth)
                        r=requests.post(url_game+ID+"/move/"+lets[m[0][0]]+str(m[0][1]+1)+lets[m[1][0]]+str(m[1][1]+1),auth=token)
                        #b.display()
                    else: side=1
                elif msg['type']=='gameState' and msg['status']=='started':
                    #check that the move made is by human.
                    moves=msg['moves'].split()
                    if len(moves)%2==side:
                        #make the move on this board.
                        if len(moves[-1])==5:
                            #promotion.
                            m=b.translate(moves[-1][0:2]+" "+moves[-1][2:4]+" "+moves[-1][4],not side)
                        #check for castles.
                        elif side==0 and moves[-1]=='e8g8' and b.Black.king.coords==[4,7]:
                            m=b.translate('O-O',not side)
                        elif side==0 and moves[-1]=='e8c8' and b.Black.king.coords==[4,7]:
                            m=b.translate('O-O-O',not side)
                        elif side==1 and moves[-1]=='e1g1' and b.White.king.coords==[4,0]:
                            m=b.translate('O-O',not side)
                        elif side==1 and moves[-1]=='e1c1' and b.White.king.coords==[4,0]:
                            m=b.translate('O-O-O',not side)
                        else:
                            #regular move.
                            m=b.translate(moves[-1][0:2]+" "+moves[-1][2:4],not side)
                        b.makemove(m,not side)
                        #b.display()
                        #now play computer move.
                        t=0
                        if side==0: t=msg['wtime']
                        else: t=msg['btime']
                        t=math.floor(t/1000)
                        print(t)
                        if t<=30: depth=2
                        else: depth=3
                        m=b.pcmove(depth)
                        a=lets[m[0][0]]+str(m[0][1]+1)+lets[m[1][0]]+str(m[1][1]+1)
                        if len(m)==4: a+=pieces[m[3]]
                        r=requests.post(url_game+ID+"/move/"+a,auth=token)
                        #b.display()
                    
                elif msg['type']=='chatLine':
                    pass
    

#the main bot loop.
while True:
    if not gameon: get_challenges(url_getevents)

    if gameon:
        #enter the game stream by ID.
        game_stream(gameID)
        #now game is over.
        gameon=False
        gameID=""
