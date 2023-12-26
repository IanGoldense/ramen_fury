import unittest
from rf_server import *


class DeckObjectTests(unittest.TestCase):
    def setUp(self):
        self.player1, self.player2, self.player3 = Player('p1'), Player('p2'), Player('p3')
        self.test_deck = Deck()
        self.test_deck.shuffle()
        self.pantry = Pantry(self.test_deck)
        self.discard_pile = DiscardPile()

    def test_deal_cards_to_players(self):
        self.test_deck.deal(self.player1, self.player2, self.player3)

        # checks each player has five cards in their hand
        for player in (self.player1, self.player2, self.player3):
            self.assertEqual(5,
                             len(player.hand),
                             f"{player.name} does not have 5 cards in their hand")

    def test_shuffle(self):
        card1, card2, card3 = self.test_deck.cards[0], self.test_deck.cards[1], self.test_deck.cards[3]
        self.test_deck.shuffle()
        card4, card5, card6 = self.test_deck.cards[0], self.test_deck.cards[1], self.test_deck.cards[3]

        self.assertNotEqual((card1, card2, card3),
                            (card4, card5, card6),
                            f"the first and second card in the deck matched, "
                            f"there's a very small chance this could naturally fail but it's very unlikely")


if __name__ == '__main__':
    unittest.main()
