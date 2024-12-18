# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 10:23:36 2024

@author: 188123
"""

import random
class Board:
    def __init__(self):
        self.spaces = []
        self.spaces.append(Go_Space())
        self.spaces.append(Property("Old Kent Road", 60, 2, "Brown"))
        self.spaces.append(Space("Community Chest")) # TODO
        self.spaces.append(Property("Whitechapel Road", 60, 4, "Brown"))
        self.spaces.append(Tax("Income Tax", 200))
        self.spaces.append(Station("King's Cross Station"))
        self.spaces.append(Property("The Angel Islington", 100, 6, "Light Blue"))
        self.spaces.append(Space("Chance")) # TODO
        self.spaces.append(Property("Euston Road", 100, 6, "Light Blue"))
        self.spaces.append(Property("Pentonville Road", 120, 8, "Light Blue"))
        self.spaces.append(Space("Just Visiting"))
        self.spaces.append(Property("Pall Mall", 140, 10, "Pink"))
        self.spaces.append(Utility("Electric Company"))
        self.spaces.append(Property("Whitehall", 140, 10, "Pink"))
        self.spaces.append(Property("Northumberland Avenue", 160, 12, "Pink"))
        self.spaces.append(Station("Marylebone Station"))
        self.spaces.append(Property("Bow Street", 180, 14, "Orange"))
        self.spaces.append(Space("Community Chest")) # TODO
        self.spaces.append(Property("Marlborough Street", 180, 14, "Orange"))
        self.spaces.append(Property("Vine Street", 200, 16, "Orange"))
        self.spaces.append(Space("Free Parking"))
        self.spaces.append(Property("Strand", 220, 18, "Red"))
        self.spaces.append(Space("Chance")) # TODO
        self.spaces.append(Property("Fleet Street", 220, 18, "Red"))
        self.spaces.append(Property("Trafalgar Square", 240, 20, "Red"))
        self.spaces.append(Station("Fenchurch St Station"))
        self.spaces.append(Property("Leicester Square", 260, 22, "Yellow"))
        self.spaces.append(Property("Coventry Street", 260, 22, "Yellow"))
        self.spaces.append(Utility("Water Works"))
        self.spaces.append(Property("Piccadilly", 280, 24, "Yellow"))
        self.spaces.append(Go_To_Jail())
        self.spaces.append(Property("Regent Street", 300, 26, "Green"))
        self.spaces.append(Property("Oxford Street", 300, 26, "Green"))
        self.spaces.append(Space("Community Chest")) # TODO
        self.spaces.append(Property("Bond Street", 320, 28, "Green"))
        self.spaces.append(Station("Liverpool St Station"))
        self.spaces.append(Space("Chance")) # TODO
        self.spaces.append(Property("Park Lane", 350, 35, "Dark Blue"))
        self.spaces.append(Tax("Super Tax", 100))
        self.spaces.append(Property("Mayfair", 400, 50, "Dark Blue"))

    def board (self): #TODO: make players appear on the board
        self.boardthatdoesthing = """
        ╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗
        ║F P║STR║CHA║FLT║TRF║FNS║LST║COV║W W║PIC║GTJ║
        ╠═══╬═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╬═══╣
        ║VIN║                                   ║REG║
        ╠═══╣                                   ╠═══╣
        ║MAR║                                   ║OXF║
        ╠═══╣                                   ╠═══╣
        ║C C║                                   ║C C║
        ╠═══╣                                   ╠═══╣
        ║BOW║                                   ║BND║
        ╠═══╣                                   ╠═══╣
        ║MBS║                                   ║LSS║
        ╠═══╣                                   ╠═══╣
        ║NOR║                                   ║CHA║
        ╠═══╣                                   ╠═══╣
        ║WHT║                                   ║PAR║
        ╠═══╣                                   ╠═══╣
        ║E C║                                   ║S T║
        ╠═══╣                                   ╠═══╣
        ║PAL║                                   ║MAY║
        ╠═══╬═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╬═══╣
        ║J V║PTV║EUS║CHA║TAI║KCS║I T║WCR║C C║OKR║G O║
        ╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝
        """
class Space:
    def __init__(self, name):
        self.name = name

    def on_land(self, player):
        pass

class Go_Space(Space):
    def __init__(self):
        Space.__init__(self, "Go")

    def on_land(self, player):
        player.add_money(200)

class Go_To_Jail(Space):
    def __init__(self):
        Space.__init__(self, "Go To Jail")

    def on_land(self, player):
        player.go_to_jail()

class Tax(Space):
    def __init__(self, name, tax):
        Space.__init__(self, name)
        self.tax = tax

    def on_land(self, player):
        player.pay_bank(self.tax)

class Property(Space):
    def __init__(self, name, cost, rent, set):
        Space.__init__(self, name)
        self.cost = cost
        self.rent = rent
        self.super_rent = rent * 2
        self.owner = None
        self.set = set

    def on_land(self, player):
        if self.owner is None:
            player.buy(self)
        else:
            player.pay(self.owner, self.rent)
            # TODO: double rent if full set owned

class Station(Property):
    def __init__(self, name):
        Property.__init__(self, name, 200, 25, "Stations")


    def on_land(self, player):
        if self.owner is None:
            player.buy(self)
        else:
            player.pay(self.owner, self.rent * (2 ** (self.owner.num_owned("Stations") - 1)))

class Utility(Property):
    def __init__(self, name):
        Property.__init__(self, name, 150, 4, "Utilities")
        self.super_rent = 10
    
    
    def on_land(self, player):
        if self.owner is None:
            player.buy(self)
        else:
            pass # TODO: pay rent = 4 x dice roll (or 10x if both owned)

# TODO: implement player logic
class Player:
    def __init__(self, name, game_piece):
        self.name = name
        self.gamer_piece = game_piece
        self.money = 1500
        self.properties = []
        self.current_space = None

    def add_money(self, amount):
        pass

    def pay_bank(self, amount):
        pass

    def pay(self, player, amount):
        pass

    def go_to_jail(self):
        pass

    
    def roll_dice(self, times: int):
            die1 = random.randint(1, 6)
            die2 = random.randint(1, 6)
            return die1 + die2

    def is_bankrupt(self):
        pass

class Game:
    def __init__(self):
        self.players_dict = {}
        self.token_array = [
                    "rex",
                    "boat",
                    "dog",
                    "thimble",
                    "shoe",
                    "car"
                    ]
    
    def player_name(self):
        print("Hello, Welcome to Monopoly. How many people are playing the game? The limit is 4.")
        
        

        num_Players = int(input("\nhow many players are in the game?: "))
        if not int(num_Players) :
            print("enter a number from 1 to 4, not a word")
        if num_Players < 1 or num_Players > 4:
            print("the limit is 4 players and must be at least one")
            return
        
        for i in range(0,num_Players): # can enter as many names as there are players inputed in the numplayers variable
            name = input("Enter player name: ")
            self.players_dict['player {}'.format(i)] = name.upper()

            print(f"tokens:{(self.token_array)}")# curley brackets othersie you cant format the text
            token = input(f"{name}, enter token you want to use: ")
            if token in self.token_array:
                self.token_array.remove(token)#removes token from list becuase there used to show who is who on the board making it confusing if there was more than one of a token
                self.players_dict[name] = token
            
            self.players = (f"{name}: {token}") #if not formatted would just output the words name and token
            print (self.players)
            
if __name__ == "__main__":
    game_instance = Game()
    game_instance.player_name()
    def setup(self):
        
        current_player = self.players[0] # TODO: have players roll 1d6 to see who goes first
        self.setup
        game_over = False
        while not game_over:
                print(self.boardthatdoesthing)
                print(f"{current_player.name}'s turn:")
                input("press enter to roll")
                current_player.move()
                current_player.current_space.on_land(current_player)
                # TODO: roll again on double, send to jail on triple-double
    
                next_player = self.players[(self.players.index(current_player) + 1) % len(self.players)]
                if current_player.is_bankrupt():
                    print(f"{current_player.name} is bankrupt!")
                    self.players.remove(current_player)
                    if len(self.players) == 1:
                        game_over = True
                current_player = next_player
    
        print(f"""
            Game over!
            {current_player.name} wins!
            They had £{current_player.money}
            """)#
            
game_instance = Game()
game_instance.start_game()
        
