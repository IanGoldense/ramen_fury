import random
import socket
from collections import deque
from icecream import ic

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

    def __determine_player_order(self, roster: list) -> tuple:
        # take in roster as a list of instantiated players

        # sort list by date last bowl of ramen was eaten

        # return tuple of instantiated players
        ...

    def next_player(self):
        # cycle through the tuple of players, this will be a cool chance to use yield
        yield


class Card:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return self.__str__()

    def __str__(self):
        # gets the first value from the class instance's dictionary of attributes
        return self.__dict__[next(iter(self.__dict__))]


class IngredientCard(Card):
    def __init__(self, ingredient):
        self.ingredient = ingredient


class Nori(IngredientCard):
    def __init__(self):
        self.flavor = 'Nori'
        self.scoring_guide = 1


class ChiliPepper(IngredientCard):
    def __init__(self):
        self.flavor = 'Chili Pepper'
        self.scoring_guide = -1  # unless with fury flavor not sure how to account for


class FlavorCard(Card):
    def __init__(self):
        self.flavor = 'plain'
        self.scoring_guide = {}


class BeefFlavor(FlavorCard):
    def __init__(self):
        self.flavor = 'Beef Flavor'
        self.scoring_guide = {
            'unique_protein1': 2,
            'unique_protein2': 5,
            'unique_protein3': 9,
            'unique_protein4': 14
        }


class SoySauceFlavor(FlavorCard):
    def __init__(self):
        self.flavor = 'SoySauce Flavor'
        self.scoring_guide = {
            'unique_veg1': 2,
            'unique_veg2': 5,
            'unique_veg3': 9,
            'unique_veg4': 14
        }


class ShrimpFlavor(FlavorCard):
    def __init__(self):
        self.flavor = 'Shrimp Flavor'
        self.scoring_guide = {
            'protein and veg': 4,
            'two protein and two veg': 8
        }


class ChickenFlavor(FlavorCard):
    def __init__(self):
        self.flavor = 'Chicken Flavor'
        self.scoring_guide = {
            "pair": 6,
            "three of a kind": 10
        }


class FuryFlavor(FlavorCard):
    def __init__(self):
        self.flavor = 'Fury Flavor'
        self.scoring_guide = (2, 4, 6, 8)


class Deck:
    def __init__(self):
        self.cards = []

        # add five of each type of ingredient card to the deck
        all_ingredients = (veg_ingredient_cards +
                           protein_ingredient_cards +
                           hybrid_ingredient_cards)

        for ingredient in all_ingredients:
            self.__add_num_of_card(5, IngredientCard(ingredient))

        # add five of each flavor card to the deck
        for flavor in FlavorCard.__subclasses__():
            self.__add_num_of_card(5, flavor())

        # add 8 Nori cards and 12 chili pepper cards
        self.__add_num_of_card(8, Nori())
        self.__add_num_of_card(12, ChiliPepper())

    def __add_num_of_card(self, num: int, card: object):
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

    def deal(self, roster):
        # everyone in the roster gets five cards
        dealer_rotation = roster * 5

        for player in dealer_rotation:
            player.draw(self.draw_one())

    def draw_one(self):
        return self.cards.pop(0)


class DiscardPile:
    def __init__(self):
        self.cards = []

    def discard(self, card):
        self.cards.append(card)


class Pantry:
    def __init__(self, deck):
        self.cards = []  # list of 4 face-up cards
        self.__build(deck)

    def __build(self, deck):
        for card in range(0, 4):
            self.cards.append(deck.draw_one())

    def restock(self):
        # discard all 4 cards

        # dr
        ...


class Bowl:
    def __init__(self):
        self.ingredients = deque(maxlen=5)
        self.eaten = False
        self.value = 0

    def eat(self):
        # total up ingredients based on flavor packet scoring guide
        pass

    def empty(self, discard_pile):
        # discard all ingredients to discard pile
        for ingredient in self.ingredients:
            discard_pile.discard(ingredient)

        # reset bowl
        self.value = 0


class Player:
    def __init__(self, name):
        self.name = name
        self.last_ate_ramen = None
        self.hand = []
        self.spoons = 2
        self.bowl1 = Bowl()
        self.bowl2 = Bowl()
        self.bowl3 = Bowl()
        self.score = 0

    def restock(self, pantry):
        pantry.cards.clear()
        pantry.restock()

    def draw(self, deck):
        self.hand.append(deck.draw_one)

    def eat(self):
        ...

    def draw_from_pantry(self, pantry, deck):
        # player chooses card from pantry
        print(f"cards in pantry: ", pantry.cards)
        picked_card = input("choose card 1 - 4: ")
        picked_card = int(picked_card) - 1

        # card is added to their hand
        self.hand.append(pantry.cards[picked_card])

        # new card is added to the pantry from the deck
        while pantry.cards < 4:
            pantry.cards.append(deck.draw_one())

    def empty_bowl(self, bowl, discard_pile):
        bowl.empty(discard_pile)

    def add_ingredient(self, ingredient, bowl):
        ...

    def play_garnish(self, player, bowl):
        ...


if __name__ == '__main__':
    # print_server_details()
    # gather_players(3)

    # testing
    test_deck = Deck()
    test_deck.shuffle()
    test_pantry = Pantry(test_deck)
    test_player = Player('Ian')
    print(test_deck.cards)
