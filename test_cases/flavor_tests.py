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


if __name__ == '__main__':
    unittest.main()
