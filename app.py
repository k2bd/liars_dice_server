#!/usr/bin/env python3

from pymongo import MongoClient
from flask import Flask, request

application = Flask(__name__)
client = MongoClient('localhost:27017')
db = client.liarsdice

@application.route("/start/<gameid>",methods=["GET"])
def startgame(gameid):
    if request.method == "GET":
        # TODO: start the game

@application.route("/config/<gameid>",methods=["GET","POST","DELETE"])
def config(gameid):
    if request.method == "POST":
        if db.Games.find_one({"game_id":gameid}).count == 0:
            # Game does not yet exist - create it
            game = 
            {
                'game_id' : gameid,
                'players' : [],
            }
            db.games.insert_one(game)
        
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