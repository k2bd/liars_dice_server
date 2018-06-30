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

        self.hand_number = 0

        self.made_bet = None

        self.last_loser = None
        self.last_result = None

    def addPlayer(self,player_name, player_id):
        if player_name in self.player_names:
            return False
        self.player_names.add(player_name)
        self.players.append(Player(player_name, player_id))
        random.shuffle(self.players)
        return True

    def makeBet(self,bet):
        if (bet[0] > self.current_bet[0]) or (bet[1] > self.current_bet[1]):
            self.current_bet = bet
            self.made_bet = self.current_turn
            self.current_turn += 1
            if self.current_turn >= len(self.players):
                self.current_turn = 0
            
            return True
        else:
            return False

    def bluff(self,bluffer_id):
        losing_player = None
        if self.totalDice(self.current_bet[1]) >= self.current_bet[0]:
            # Bluff was unsuccessful
            for player in self.players:
                if player.player_id = bluffer_id:
                    losing_player = player
        else:
            # Bluff was successful
            losing_player = self.players[self.made_bet]
        
        self.last_loser = losing_player.player_name
        losing_player.totalDice -= 1
        self.newHand()

    def totalDice(self,rank):
        total = 0
        for player in self.players:
            total += player.dice[rank-1]
        return total
    
    def newHand(self):
        self.hand_number += 1

        self.last_result = [0,0,0,0,0,0]
        for i in range(6):
            self.last_result[i] = self.totalDice(i+1)
        
        for player in self.players:
            new_dice = [0,0,0,0,0,0]
            for i in range(player.dice_left):
                new_dice[random.randint(0,5)] += 1


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
        if gameid not in games:
            return jsonify(status="Error", message="Game does not exist!")
        
        try:
            bluff_call = request.json['bluff_call']
            bet = request.json['bet']
        except Exception as e:
            return jsonfify(status="Error",message=e)

        game = games[gameid]
        if bluff_call:
            game.bluff_call(playerid)
            return jsonify(status="OK",message="")

        if game.players[game.current_turn].player_id == playerid:
            if game.makeBet(bet):
                return jsonify(status="OK",message="")
            else:
                return jsonify(status="Error",message="Invalid bet.")
        else:
            return jsonify(status="Error",message="Not your turn")
        print(request.json)
    if request.method == "GET":
        if gameid not in games:
            return jsonify(status="Error", message="Game does not exist!")
        
        game = games[gameid]

        player = None
        for p in game.players:
            if playerid == p.player_id:
                player = p
        if player is None:
            return jsonify(status="Error",message="Player has not joined this game")

        response = {
            'hand_number' : game.hand_number,
            'dice'        : player.dice,
            'turn'        : game.players[game.current_turn].player_name
            'current_bet' : game.current_bet,
            'prev_loser'  : game.prev_loser,
            'prev_values' : game.prev_values,
        }
        
        return jsonify(response)
    if request.method == "DELETE":
        # Leave a game
        pass

if __name__=="__main__":
    application.run(host='0.0.0.0')