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


    def test_add_ingredients_to_bowl(self):
        beef, naruto = BeefFlavor(), IngredientCard('Naruto')

        for _ in (beef, naruto):
            self.player.add_ingredient(_, self.player.bowl1)

        self.assertIsInstance(self.player.bowl1.ingredients[0],
                              FlavorCard,
                              "expected card was not a flavor card ")

        self.assertIsNotNone(self.player.bowl1.flavor,
                             "the bowl's flavor was not assigned after adding a flavor card")

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

        print(mock_object)
        expected_card = self.pantry.cards[0]

        # side effect picks the first card from pantry. mock_object is implicitly used here
        self.player.draw_from_pantry(self.pantry, self.deck)

        actual_card = self.player.hand[0]

        self.assertEqual(expected_card,
                         actual_card,
                         f"card in hand ({actual_card}) does not match card found in"
                         f" pantry before selection ({expected_card})")


if __name__ == '__main__':
    unittest.main()
