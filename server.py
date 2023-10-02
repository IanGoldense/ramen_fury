import socket

###########
# Globals #
###########

protein_ingredient_cards = ("Naruto", "Eggs", "Chashu")
hybrid_ingredient_cards = ("Tofu")
veg_ingredient_cards = ("Mushrooms", "Scallions", "Corn")
garnish_cards = ("Chili Peppers", "Nori")
flavor_packets = ("Fury", "Soy Sauce", "Beef", "Chicken", "Shrimp")


#############
# Functions #
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

class Card:
    def __init__(self, card_type, ):
        self.card_type = card_type,


class Deck:
    def __init__(self):
        # five of each
        self.vegetable_cards = None
        self.protein_cards = None
        self.hybrid_cards = None

        # five of each
        self.beef_flavor = None
        self.shrimp_flavor = None
        self.soy_sauce_flavor = None
        self.chicken_flavor = None
        self.fury_flavor = None

        self.nori_cards = 8
        self.chili_peppers = 12

    def shuffle(self):
        ...

    def cut(self):
        ...

    def sort(self):
        ...

    def deal(self):
        ...

    def draw_one(self):
        ...


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


if __name__ == '__main__':
    print_server_details()
    gather_players(3)
