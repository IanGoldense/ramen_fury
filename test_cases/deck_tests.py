import builtins
import unittest
from unittest.mock import patch
from rf_server import *


class DeckObjectTests(unittest.TestCase):
    def setUp(self):
        self.player1, self.player2, self.player3 = Player('p1'), Player('p2'), Player('p3')
        self.test_deck = Deck()
        self.pantry = Pantry(self.test_deck)
        self.discard_pile = DiscardPile()

    def test_deal_cards_to_players(self):
        self.test_deck.deal(self.player1, self.player2, self.player3)

        self.assertEqual(5,
                         len(self.player1.hand),
                         "player 1 does not have 5 cards in their hand")


if __name__ == '__main__':
    unittest.main()
