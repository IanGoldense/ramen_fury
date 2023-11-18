import unittest
from rf_server import *


# TODO: may need to write this as generic tests and inherit them for each type of flavor packet since calculate_score is
#  so different for each one. swap the tests between these two classes and make the ingredients a parameter?
class FlavorPacketTests(unittest.TestCase):
    def setUp(self):
        self.player = Player('crash test dummy')

    def test_eat_bowl(self):
        self.player.eat(self.player.bowl1)

        self.assertTrue(self.player.bowl1.eaten,
                        "bowl.eaten does not equal True after being eaten.")


class ChickenFlavorTests(FlavorPacketTests):
    def setUp(self):
        # build bowl
        self.player = Player('clicky chicken')
        chicken, mushroom1, mushroom2 = ChickenFlavor(), IngredientCard("Mushrooms"), IngredientCard("Mushrooms")

        for _ in (chicken, mushroom1, mushroom2):
            self.player.add_ingredient(_, self.player.bowl1)


class FuryFlavorTests(FlavorPacketTests):
    def setUp(self):
        self.player = Player('Spicy shogun')
        fury_flavor, chili = FuryFlavor(), IngredientCard("Chili Peppers")

        for _ in (fury_flavor, chili, chili, chili):
            self.player.add_ingredient(_, self.player.bowl1)

    def test_nori_and_chili_equal_zero(self):
        """test adds a chili pepper and a nori garnish with a beef flavor, which shoudl equal 0.
         this tests the bowl.count_nori_and_chili method"""
        # instantiate
        discard = DiscardPile()
        chili, nori, beef_flavor = ChiliPepper(), Nori(), BeefFlavor()

        # add ingredients to bowl
        self.player.bowl1.empty(discard)
        for _ in (chili, nori, beef_flavor):
            self.player.add_ingredient(_, self.player.bowl1)

        self.assertEqual()

    def test_count_nori_and_chili_with_fury_flavor(self):
        # add a nori
        test_nori = Nori()
        self.player.add_ingredient(test_nori, self.player.bowl1)

        self.player.bowl1.eat()

        self.assertEqual(7,
                         self.player.bowl1.score,
                         "bowl score did not get totalled correctly. three chili and a nori should be 7 points")


if __name__ == '__main__':
    unittest.main()
