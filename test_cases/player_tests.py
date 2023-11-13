import unittest
from rf_server import *


class PlayerObjectTests(unittest.TestCase):
    def test_add_ingredients_to_bowl(self):
        player = Player('crash test dummy')
        beef = BeefFlavor()
        tofu = IngredientCard('Naruto')

        for _ in (beef, tofu):
            player.add_ingredient(_, player.bowl1)

        self.assertIsInstance(player.bowl1.ingredients[0],
                              FlavorCard,
                              "expected card was not a flavor card ")

        self.assertIsNotNone(player.bowl1.flavor,
                             "the bowl's flavor was not assigned after adding a flavor card")

    # TODO: NEED TO write test CASE FOR THE elif scenario of the bowls add_ingredient method

if __name__ == '__main__':
    unittest.main()
