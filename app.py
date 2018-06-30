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
        self.dice_left = 5
        self.dice = [0,0,0,0,0,0]

class LiarsDiceGame:
    def __init__(self, game_id):
        self.game_id = game_id
        self.player_names = set()
        self.players = []
        self.current_turn = 0
        self.current_bet = [0,0] # number, rank

    def addPlayer(self,player_name, player_id):
        if player_name in self.player_names:
            return False
        self.player_names.add(player_name)
        self.players.append(Player(player_name, player_id))
        random.shuffle(self.players)
        return True

games = {}

@application.route("/start/<gameid>",methods=["GET","POST"])
def startgame(gameid):
    if request.method == "GET":
        # TODO: start the game
        pass

@application.route("/config/<gameid>",methods=["GET","POST","DELETE"])
def config(gameid):
    if request.method == "POST":
        if gameid not in games:
            # Game does not yet exist - create it
            games[gameid] = LiarsDiceGame(gameid)

        # Now insert this player
        try:
            player_name = request.json['name']
            player_id   = request.json['id']
            if not games[gameid].addPlayer(player_name,player_id):
                return jsonify(status="Error",message="Player name already taken.")
        except Exception as e:
            return jsonify(status="Error",message=e)

        return jsonify(status="OK",message="Joined Game")
        
    if request.method == "GET":
        players_status = []
        for player in games[gameid].players:
            players_status.append({'name' : player.player_name, 'dice_left' : player.dice_left})
        return jsonify(players=players_status)
    if request.method == "DELETE":
        pass
        # Destroy a game

@application.route("/game/<gameid>/<playerid>",methods=['GET','POST','DELETE'])
def game(gameid,playerid):
    if request.method == "POST":
        # Update game with ID gameid
        pass
    if request.method == "GET":
        # TODO:
        return jsonify(status="OK",message="Game ID:"+str(gameid)+", Player ID:"+str(playerid))
    if request.method == "DELETE":
        # Leave a game
        pass

if __name__=="__main__":
    application.run(host='0.0.0.0')