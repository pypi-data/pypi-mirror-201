import unittest
from unittest import TestCase

from mo_osrs_highscores import Highscores
from mo_osrs_highscores.Exceptions import NameNotFoundException
from mo_osrs_highscores.pageparser import ParsePage


class MyTestCase(unittest.TestCase):

    def test_error(self):
        with self.assertRaises(NameNotFoundException):
            ParsePage.request_page('y7nh56')

    def test_lookup(self):
        stats = Highscores.getHighScores("rsb perpdoom")

        print(stats.HighScores)
        print(stats.Boss)
        print(stats.Skills)
        print(stats.MiniGames)
