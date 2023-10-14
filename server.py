import random
import socket

###########
# Globals #
###########

protein_ingredient_cards = ("Naruto", "Eggs", "Chashu")
hybrid_ingredient_cards = ("Tofu",)
veg_ingredient_cards = ("Mushrooms", "Scallions", "Corn")
garnish_cards = ("Chili Peppers", "Nori")
flavor_packets = ("Fury", "Soy Sauce", "Beef", "Chicken", "Shrimp")


#############
# Functions
#############

def print_server_details():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    print(f'=== server details ===')
    print(f'hostname: ', hostname)
    print(f'IP address: ', ip_address)


def gather_players(player_count: int, lobby_open: int = 60):
    # validate player count
    if player_count not in (2, 3, 4, 5):
        raise IndexError

    # get the hostname
    host = socket.gethostname()
    port = 5433

    # instantiate, then bind hostname and port
    server_socket = socket.socket()
    server_socket.bind((host, port))  # look closely. The bind() function takes tuple as argument

    # wait for players
    server_socket.listen(player_count)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        # if not data:
        #     # if data is not received break
        #     break
        print("from connected user: " + str(data))

        # data can be sent back to client here
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client


def send_message(connection, message: str):
    for user in users:
        connection.send(message.encode())  # send data to the client


###########
# Classes #
###########

class Game:
    def __init__(self, num_players: int, roster: list):
        self.num_players = num_players
        self.roster = roster
        self.active_player = None
        self.player_order = None

    def __determine_player_order(self, roster) -> tuple:
        # take in roster as a list of instantiated players

        # sort list by date last bowl of ramen was eaten

        # return tuple of instantiated players
        ...

    def next_player(self):
        # cycle through the tuple of players, this will be a cool chance to use yield
        ...


class Card:
    def __init__(self):
        pass

    def __str__(self):
        # gets the first value from the class instance's dictionary of attributes
        return self.__dict__[next(iter(self.__dict__))]


class IngredientCard(Card):
    def __init__(self, ingredient):
        self.ingredient = ingredient


class FlavorCard(Card):
    def __init__(self):
        self.flavor = 'plain'
        self.scoring_guide = {}


class BeefFlavor(FlavorCard):
    def __init__(self):
        self.scoring_guide = {
            'unique1': 2,
            'unique2': 5,
            'unique3': 9,
            'unique4': 14
        }


class FuryFlavor(FlavorCard):
    def __init__(self):
        self.scoring_guide = (2, 4, 6, 8)


class Deck:
    def __init__(self):
        self.cards = []

        self.cards.append(Card())  # TODO: delete this line later

        # add five of each type of ingredient card to the deck
        all_ingredients = veg_ingredient_cards + protein_ingredient_cards + hybrid_ingredient_cards
        for ingredient in all_ingredients:
            self._add_num_of_card(5, IngredientCard(ingredient))

        # add five of each flavor type to the deck
        for flavor in FlavorCard.__subclasses__():
            self._add_num_of_card(5, flavor)

        # five of each. should be covered once all subclasses are built.
        self.beef_flavor = None
        self.shrimp_flavor = None
        self.soy_sauce_flavor = None
        self.chicken_flavor = None
        self.fury_flavor = None

        self.nori_cards = 8
        self.chili_peppers = 12

    def _add_num_of_card(self, num: int, card: object):
        card_group = []
        for i in range(0, num):
            self.cards.append(card)

        return card_group

    def shuffle(self):
        random.shuffle(self.cards)

    def cut(self):
        top_half = self.cards[:len(self.cards) // 2]
        bottom_half = self.cards[len(self.cards) // 2:]

        self.cards = bottom_half + top_half

    def deal(self):
        ...

    def draw_one(self):
        return self.cards.pop(0)


class DiscardPile:
    def __init__(self):
        self.cards = []  # should be converted to a stack later on.


class Pantry:
    def __init__(self):
        self.cards = None  # list of 4 face-up cards


class Bowl:
    def __init__(self):
        self.eaten = False
        self.ingredients = []  # should likely be a stack later
        self.value = 0

    def eat(self):
        ...

    def empty(self):
        ...


class Player:
    def __init__(self, name):
        self.name = name
        self.last_ate_ramen = None
        self.spoons = 2
        self.bowls = {}
        self.hand = []

    def restock(self):
        ...

    def draw(self):
        ...

    def eat(self):
        ...

    def draw_from_pantry(self):
        ...

    def empty_bowl(self):
        ...

    def add_ingredient(self):
        ...

    def play_garnish(self):
        ...


if __name__ == '__main__':
    # print_server_details()
    # gather_players(3)

    # testing
    test_deck = Deck()
    print(test_deck.cards)
