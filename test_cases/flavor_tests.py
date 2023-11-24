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
        """creates a player with fury packet and three chili cards in bowl 1"""
        self.player = Player('Spicy shogun')
        fury_flavor, chili = FuryFlavor(), ChiliPepper()

        for _ in (fury_flavor, chili, chili, chili):
            self.player.add_ingredient(_, self.player.bowl1)

    def test_nori_and_chili_equal_zero(self):
        """test adds a chili pepper and a nori garnish with a beef flavor, which should equal 0.
         this tests the bowl.count_nori_and_chili method"""
        # instantiate
        discard_pile = DiscardPile()
        chili, nori, chicken_flavor = ChiliPepper(), Nori(), ChickenFlavor()

        # empty setUp bowl, add ingredients to bowl
        self.player.bowl1.empty(discard_pile)

        for _ in (chili, nori, chicken_flavor):
            self.player.add_ingredient(_, self.player.bowl1)

        self.player.bowl1.eat()

        print(f'bowl score: {self.player.bowl1.value}')

        self.assertEqual(0,
                         self.player.bowl1.value,
                         "bowl not equal to zero. ingredients were not counted correctly.")

    def test_count_nori_and_chili_with_fury_flavor(self):
        # add a nori
        test_nori = Nori()
        self.player.add_ingredient(test_nori, self.player.bowl1)

        points_scored = self.player.bowl1.eat()
        print(f"points scored: {points_scored}")

        self.assertEqual(7,
                         self.player.bowl1.value,
                         "bowl score did not get totalled correctly. three chili and a nori should be 7 points")


if __name__ == '__main__':
    unittest.main()
