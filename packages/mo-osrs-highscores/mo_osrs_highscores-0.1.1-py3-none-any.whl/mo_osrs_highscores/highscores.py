from .Exceptions import NameNotFoundException
from .pageparser import ParsePage
from .resources import BallsAndPenis


class Highscores:

    @staticmethod
    def getHighScores(playerName):
        try:
            ParsePage.request_page(playerName)
            BallsAndPenis.getMegaDic()
            return BallsAndPenis
        except NameNotFoundException:
            return

