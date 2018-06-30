#!/usr/bin/env python3

from pymongo import MongoClient
from flask import Flask, jsonify,json,request
import random

application = Flask(__name__)

# TODO: Statelessify this with mongo
#client = MongoClient('localhost:27017')
#db = client.liarsdice

class Player:
    def __init__(self,name,player_id):
        self.player_name = name
        self.player_id = player_id

class LiarsDiceGame:
    def __init__(self, game_id):
        self.game_id = game_id
        self.players = [] # Players, in turn order
        self.current_turn = 0
        self.current_bet = [0,0] # number, rank

    def addPlayer(self,Player):
        self.players.append(Player)
        random.shuffle(self.players)

games = set()

@application.route("/start/<gameid>",methods=["GET"])
def startgame(gameid):
    if request.method == "GET":
        # TODO: start the game

@application.route("/config/<gameid>",methods=["GET","POST","DELETE"])
def config(gameid):
    if request.method == "POST":
        if gameid not in games:
            # Game does not yet exist - create it
            games.insert(LiarsDiceGame(gameid))

        # Now insert this player
        try:
            player_name = request.json['name']
            player_id   = request.json['id']
            games[gameid].addPlayer(Player(player_name,player_id))
        except Exception,e:
            print(e)
        
    if request.method == "GET":
        # Get game state
    if request.method == "DELETE":
        # Destroy a game

@application.route("/game/<gameid>/<playerid>",methods=['GET','POST','DELETE'])
def game(gameid,playerid):
    if request.method == "POST":
        # Update game with ID gameid
    if request.method == "GET":
        # Get the game state
    if request.method == "DELETE":
        # Leave a game

if __name__=="__main__":
    application.run(host='0.0.0.0')