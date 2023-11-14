import unittest
from rf_server import *


# TODO: may need to write this as generic tests and inherit them for each type of flavor packet since calculate_score is
#  so different for each one
class FlavorPacketTests(unittest.TestCase):
    def test_bowl_gets_scored_on_eat(self):
        """
        ensure the bowl score gets updated in al lnecessary places after eating it
        """
        pass

    def test_calculate_score(self):
        """
        make sure the flavor packet calculates score based on the ingredients in the bowl.
        """
        pass


class ChickenFlavorTests(FlavorPacketTests):
    def setUp(self):
        # build bowl
        self.player = Player('clicky chicken')
        chicken, mushroom1, mushroom2 = ChickenFlavor(), IngredientCard("Mushrooms"), IngredientCard("Mushrooms")

        for _ in (chicken, mushroom1, mushroom2):
            self.player.add_ingredient(_, self.player.bowl1)

    def test_eat_bowl(self):
        self.player.eat(self.player.bowl1)

        self.assertEqual(self.player.score,
                         6,
                         "player did not score 6 points for eating a bowl of ramen")


if __name__ == '__main__':
    unittest.main()
