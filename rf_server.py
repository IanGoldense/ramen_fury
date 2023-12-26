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
    def __call__(self, *args, **kwargs) -> str:
        return self.__str__()

    def __str__(self) -> str:
        """
        gets the first value from the class instance's dictionary of attributes
        i.e. makes every card str() the name of it's class
        :return: name of the object's class type in string form
        """
        return self.__dict__[next(iter(self.__dict__))]

    def __repr__(self):
        """makes any call to the memory address of the object return it's class name"""
        return self.__str__()


class IngredientCard(Card):
    def __init__(self, ingredient):
        self.ingredient = ingredient


class Nori(Card):
    def __init__(self):
        self.flavor = 'Nori'
        self.scoring_guide = 1


class ChiliPepper(Card):
    def __init__(self):
        self.flavor = 'Chili Pepper'
        self.scoring_guide = -1  # unless with fury flavor, not sure how to account for


class FlavorCard(Card):
    def __init__(self):
        self.flavor = 'plain'
        self.scoring_guide = {}

    def calc_score_for_unique_ingredients(self, ingredients: deque):
        pass
        # this could be a shared method between the Beef and SoySauce classes, but that requires a more complex method,
        # so i am building a janky first version for now to get it working.


class BeefFlavor(FlavorCard):
    def __init__(self):
        self.flavor = 'Beef Flavor'
        self.scoring_guide = {
            0: 0,  # nothing in the bowl =(
            1: 2,  # 1 unique protein
            2: 5,  # 2 unique protein
            3: 9,  # 3 unique protein
            4: 14  # 4 unique protein
        }

    def calculate_score(self, ingredients: deque) -> int:
        """
        called by a Bowl object when calculating the score to return the value of all the ingredients.
        :param ingredients: stack object of all ingredients that have been added to the bowl.
        :return: int. value of the bowl. should be added to the player.score attribute.
        """

        # build set of unique veg ingredients
        unique_proteins = set()
        for card in ingredients:
            if card.ingredient in protein_ingredient_cards:
                unique_proteins.add(card)

        # dictionary lookup with index equal to length of unique ingredient set
        return self.scoring_guide[len(unique_proteins)]


class SoySauceFlavor(FlavorCard):
    def __init__(self):
        self.flavor = 'SoySauce Flavor'
        self.scoring_guide = {
            0: 0,  # nothing in the bowl =(
            1: 2,  # 1 unique veg
            2: 5,  # 2 unique veg
            3: 9,  # 3 unique veg
            4: 14  # 4 unique veg
        }

    def calculate_score(self, ingredients: deque) -> int:
        """
        called by a Bowl object when calculating the score to return the value of all the ingredients.
        :param ingredients: stack object of all ingredients that have been added to the bowl.
        :return: int. value of the bowl. should be added to the player.score attribute.
        """

        # build set of unique veg ingredients
        unique_veg = set()
        for card in ingredients:
            if card.ingredient in veg_ingredient_cards:
                unique_veg.add(card)

        # dictionary lookup with index equal to length of ingredient set
        return self.scoring_guide[len(unique_veg)]


class ShrimpFlavor(FlavorCard):
    def __init__(self):
        self.flavor = 'Shrimp Flavor'
        self.scoring_guide = {
            'protein and veg': 4,
            'two protein and two veg': 8
        }

    def calculate_score(self, ingredients: deque) -> int:
        pass
        # # if ingredients contains a veg and a protein
        #
        # # if ingredients contains two veg and two proteins


class ChickenFlavor(FlavorCard):
    def __init__(self):
        self.flavor = 'Chicken Flavor'
        self.scoring_guide = {
            "pair": 6,
            "three of a kind": 10
        }

    def calculate_score(self, ingredients: deque) -> int:
        score = 0
        ingredient_counts = {}

        # Count occurrences of each ingredient, less chili or nori
        for card in ingredients:
            if isinstance(card, IngredientCard) and not isinstance(card, ChiliPepper):
                ingredient = card.ingredient
                if ingredient in ingredient_counts:
                    ingredient_counts[ingredient] += 1
                else:
                    ingredient_counts[ingredient] = 1

        # Apply scoring logic
        for count in ingredient_counts.values():
            if count == 2:
                score += self.scoring_guide['pair']
            elif count >= 3:
                score += self.scoring_guide['three of a kind']

        return score


class FuryFlavor(FlavorCard):
    def __init__(self):
        self.flavor = 'Fury Flavor'
        self.scoring_guide = (2, 4, 6, 8)

    def calculate_score(self, ingredients: deque) -> int:
        score = 0
        for _ in ingredients:
            if isinstance(_, ChiliPepper):
                score += 2

        return score


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

    def __add_num_of_card(self, num: int, card: Card):
        """
        appends num of cards to the self.cards attribute. Used when generating a deck.
        :param num: number of cards to be added.
        :param card: card type to be added.
        :return: None.
        """
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

    # this string type hint is a stupid python 3.10 change. PEP 563 was going to enable 'postponed evaluation of
    # annotations' but it was pulled last second. Python 3.6 implements string literal annotations so use that.
    def deal(self, *players: 'Player') -> None:
        """
        deal five cards to each player.
        :param players: instances of Player class. should be no more than five players as-per game rules.
        :return: none.
        """
        for player in (players * 5):
            player.draw(self)

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
        self.__fill_pantry(deck)

    def __call__(self, *args, **kwargs):
        return self.__str__()

    def __str__(self) -> str:
        card_names = ''
        for card in self.cards:
            card_names += f' {str(card)}'

        return card_names

    def __fill_pantry(self, deck):
        for card in range(0, 4):
            self.cards.append(deck.draw_one())

    def restock(self, deck, discard_pile):
        """
        Remove all the cards from the Pantry and replace them with four new ones from the deck.
        The special abilities on any Chili Peppers or Nori Garnish are activated when a player restocks.
        :param deck: deck instance. new pantry cards are drawn from deck.
        :param discard_pile: discard_pile instance. Old pantry cards are moved to here
        :return:
        """
        # move old cards to the discard pile
        for card in self.cards:
            discard_pile.discard(card)

        self.cards.clear()
        self.__fill_pantry(deck)

        # TODO: give player the option to play any chili pepper or nori garnish that is dran from the pantry in this way


class Bowl:
    def __init__(self):
        self.ingredients = deque(maxlen=5)
        self.eaten = False
        self.flavor = None
        self.value = 0

    def __str__(self):
        # TODO: this could be beautified a lot more to print a comprehensive list of bowl ingredients
        return str(self.ingredients)

    def __iter__(self):
        return self.ingredients[::-1]

    def __count_nori_and_chili(self) -> int:
        """counts the nori and chili pepper cards in the ingredients stack"""
        points = 0
        for nori in self.ingredients:
            if isinstance(nori, Nori):
                points += 1

        if self.ingredients.__contains__(FuryFlavor()):
            for chili in self.ingredients:
                if isinstance(chili, ChiliPepper):
                    points -= 1

        return points

    def eat(self) -> None:
        """
        A Ramen Bowl must have one Flavor Ingredient and at least one other ingredient before it can be eaten.
        A bowl that has been eaten cannot have more ingredients added or taken away.
        :return: static function. sets bowl attributes
        """
        if self.eaten is False and self.flavor is not None and len(self.ingredients) >= 2:
            score = self.flavor.calculate_score(self.ingredients)
            score += self.__count_nori_and_chili()
            self.eaten = True
            self.value += score

        elif self.eaten is True:
            raise Exception("bowl has already been eaten.")

        else:
            raise Exception("bowl must have a flavor ingredient and one other ingredient.")

    def empty(self, discard_pile) -> None:
        """remove all ingredients from bowl, move them to discard pile and reset point value"""
        [discard_pile.discard(ingredient) for ingredient in self.ingredients]
        self.ingredients.clear()
        self.flavor = None
        self.value = 0


class Player:
    def __init__(self, name):
        self.name = name
        self.last_ate_ramen = None  # TODO: make this a parameter later, or call the function
        self.hand = []
        self.spoons = 2
        self.bowl1 = Bowl()
        self.bowl2 = Bowl()
        self.bowl3 = Bowl()
        self.score = 0

    def restock(self, pantry, discard_pile) -> None:
        pantry.restock(pantry, discard_pile)

    def draw(self, deck: Deck):
        self.hand.append(deck.draw_one())

    def eat(self, bowl):
        self.score += bowl.eat()

    def draw_from_pantry(self, pantry, deck):
        """
        asks the player to choose a card from the pantry and adds it to their hand.
        :param pantry: pantry object.
        :param deck: deck object.
        :return: None
        """
        # player chooses card from pantry
        print(f"cards in pantry: ", pantry.cards)

        # sanitize input
        picked_card = 0
        valid_choices = (1, 2, 3, 4)
        while picked_card not in valid_choices:
            picked_card = input("choose card 1 - 4: ")
            print("invalid choice, try again.") if picked_card not in valid_choices else None

        # move input value back one int to align with the list index
        picked_card = int(picked_card) - 1

        # card is added to their hand and removed from the pantry
        self.hand.append(pantry.cards[picked_card])
        pantry.cards.remove(pantry.cards[picked_card])

        # new card is added to the pantry from the deck, bringing it up to 4 cards
        while len(pantry.cards) < 4:
            pantry.cards.append(deck.draw_one())

    def empty_bowl(self, bowl, discard_pile):
        bowl.empty(discard_pile)

    def add_ingredient(self, ingredient, bowl) -> None:
        """
        player moves an ingredient from their hand to a bowl.
        :param ingredient: ingredient card to be added to the bowl.
        :param bowl: one of the player's bowl objects. must be the player's own bowls.
        :return: None
        """
        # ensure player is only adding to their own bowl
        if bowl not in (self.bowl1, self.bowl2, self.bowl3):
            raise ValueError("You can only add ingredients to your own bowls.")

        # adding a flavor packet, declares bowl flavor and determines scoring guide
        # checks if ingredient is a subclass of FlavorCard
        if issubclass(ingredient.__class__, FlavorCard) and bowl.flavor is None:
            bowl.flavor = ingredient
            bowl.ingredients.append(ingredient)

        # prevent multiple flavor packets from being added to bowl
        elif issubclass(ingredient.__class__, FlavorCard) and bowl.flavor is not None:
            raise Exception("cannot add more than one flavor packet to a bowl.")

        # add normal ingredients
        else:
            bowl.ingredients.append(ingredient)

        self.hand.remove(ingredient)

    def play_garnish(self, player):
        """
        player adds a Nori garnish card from their hand to another player's bowl of their choice.
        :param player: opponent player.
        :return:
        """
        # dict lookup. Map opponent player's bowls to integers we get from the input() later
        bowl_dict = {
            1: player.bowl1,
            2: player.bowl2,
            3: player.bowl3
        }

        # if any held card is an instance of Nori, ask which bowl should receive it.
        if any(isinstance(card, Nori) for card in self.hand):
            bowl = None
            while bowl not in (1, 2, 3):
                print(f"{player.name}'s bowls. input 1,2 or 3:"
                      f"{player.bowl1}"
                      f"{player.bowl2}"
                      f"{player.bowl3}")
                bowl = input("where to play garnish?")

            # add nori card to opponent players bowl and remove it from active players hand
            player.add_ingredient(Nori(), bowl_dict[bowl])

        else:
            print("player does not have a Nori card")


# if __name__ == '__main__':
ian, emily, maxy, beans, kayla = Player('Ian'), Player('Emily'), Player('Maxy'), Player('Beans'), Player('Kayla')
deck, discard_pile = Deck(), DiscardPile()
pantry = Pantry
