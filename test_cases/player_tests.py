import unittest
from rf_server import *


class PlayerObjectTests(unittest.TestCase):
    def test_add_ingredients_to_bowl(self):
        player = Player('crash test dummy')
        beef = BeefFlavor()
        naruto = IngredientCard('Naruto')

        for _ in (beef, naruto):
            player.add_ingredient(_, player.bowl1)

        self.assertIsInstance(player.bowl1.ingredients[0],
                              FlavorCard,
                              "expected card was not a flavor card ")

        self.assertIsNotNone(player.bowl1.flavor,
                             "the bowl's flavor was not assigned after adding a flavor card")

    def test_add_multiple_flavors_to_bowl(self):
        """
        add two types of flavor packets to a player's bowl to ensure we raise an error.
        """
        player = Player('crash test dummy')
        beef, shrimp, naruto = BeefFlavor(), ShrimpFlavor(), IngredientCard('Naruto')

        with self.assertRaises(Exception):
            for _ in (beef, shrimp, naruto):
                player.add_ingredient(_, player.bowl1)


if __name__ == '__main__':
    unittest.main()
