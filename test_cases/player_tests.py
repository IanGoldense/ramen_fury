import builtins
import unittest
from unittest.mock import patch
from rf_server import *


class PlayerObjectTests(unittest.TestCase):
    def setUp(self):
        self.player = Player('crash test dummy')
        self.deck = Deck()
        self.deck.shuffle()
        self.pantry = Pantry(self.deck)

    def test_draw_from_deck(self):
        self.player.draw(self.deck)
        self.assertIsInstance(self.player.hand[0],
                              Card,
                              "player did not get a card placed into their hand when drawing from the deck")

    def test_add_ingredients_to_bowl(self):
        beef, naruto = BeefFlavor(), IngredientCard('Naruto')

        for _ in (beef, naruto):
            self.player.add_ingredient(_, self.player.bowl1)

        self.assertIsInstance(self.player.bowl1.ingredients[0],
                              FlavorCard,
                              "expected card was not a flavor card ")

        self.assertIsNotNone(self.player.bowl1.flavor,
                             "the bowl's flavor was not assigned after adding a flavor card")

    def test_card_removed_from_hand(self):
        mushroom_deck = Deck()
        self.player.draw(mushroom_deck)  # gives player a mushroom card
        self.player.add_ingredient(self.player.hand[0], self.player.bowl1)

        self.assertNotIn(mushroom_deck.cards[0],
                         self.player.hand,
                         f"mushroom was not removed from players hand after being played."
                         f" player's hand: {self.player.hand}")

    def test_add_multiple_flavors_to_bowl(self):
        """
        add two types of flavor packets to a player's bowl to ensure we raise an error.
        """
        beef, shrimp, naruto = BeefFlavor(), ShrimpFlavor(), IngredientCard('Naruto')

        with self.assertRaises(Exception):
            for _ in (beef, shrimp, naruto):
                self.player.add_ingredient(_, self.player.bowl1)

    @patch('builtins.input', side_effect=[1])
    def test_draw_from_pantry(self, mock_object):
        """player draws from pantry and adds to hand. test pantry refills, and hand updates"""
        expected_card = self.pantry.cards[0]

        # @patch and side effect picks the first card from pantry. mock_object is implicitly used here
        # because player.draw_from_pantry is the method calling input()
        self.player.draw_from_pantry(self.pantry, self.deck)

        actual_card = self.player.hand[0]

        self.assertEqual(expected_card,
                         actual_card,
                         f"card in hand ({actual_card}) does not match card found in"
                         f" pantry before selection ({expected_card})")

    @patch('builtins.input', side_effect=[1])
    def test_play_garnish(self, mock_object):
        self.target_player = Player('Bob Bastard')
        self.player.play_garnish(self.target_player)
        test_nori = Nori()
        test_chili = ChiliPepper()

        self.player.hand.append(Nori())  # give the player cards to play
        self.player.hand.append(test_chili)
        self.player.play_garnish(self.target_player)  # play garnish card into target_player hand. @Patch used here

        # assert nori was removed from player 1's hand
        self.assertNotIn(test_nori,
                         self.player.hand,
                         f'players hand was not an empty list. Player is holding: {self.player.hand}.')

        print(f"debug: {self.target_player.bowl1.ingredients}")
        # assert player 2 has a nori
        self.assertIn(test_nori,
                      self.target_player.bowl1.ingredients,
                      'a nori was not found in opponents hand')


if __name__ == '__main__':
    unittest.main()
