# Web API:
## `/game/<gameid>/<playerid>`
### `GET`
Returns the current game state as viewed by playerid
PlayerID is NOT player name, it's a secret ID.
```
{
    'dice'        : [0,0,2,1,0,1], // How many of each dice value the player has. In this case, 2 3's, a 4, and a 6.
    'turn'        : 'Kevin',       // Whose turn it is
    'current_bet' : [1,5]          // Current bet, in this case one 5
    'prev_loser'  : "Kevin"        // In the previous round, which player lost a die
    'prev_values' : [4,3,2,1,4,6]  // In the previous round, how many of each dice value there were
}
```
### `POST`
A player makes a turn by posting something of the following format:
```
{
    'bet'        : [4,5] // Number and value of bet. In this case 4 5's
    'bluff_call' : False // True if the player is calling a bluff and False if they want to make the above bet.
                         // Bet is ignored if bluff_call is True
}
```
This will return OK if the move is accepted, or the following error code if not:
 - ???? - Not your turn
 - ???? - Bet Invalid
 - ???? - Not allowed to call blufff, e.g. on first turn.
### `DELETE`
A player wants to leave the game.

## `/config/<gameid>`
### `GET`
Returns the current game config
```
{
    'players' : 
        [
            {
                'name' : 'Kevin',
                'dice_left' : 2,
            },
            {
                'name' : 'Mark',
                'dice_left' : 5,
            },
            {
                'name' : 'Brett',
                'dice_left' : 4,
            }
        ]
}
```
### `POST`
Join a game by posting:
```
{
    'name' : 'Mr. E' // Name you'd like to take in the game
    'id'   : '123e4567-e89b-12d3-a456-426655440000' // A randomly generated secret ID string used for API calls. No spaces.
}
```
Will return OK if you joined successfully, or error code ???? if the name was taken.
### `DELETE`
Delete an entire game