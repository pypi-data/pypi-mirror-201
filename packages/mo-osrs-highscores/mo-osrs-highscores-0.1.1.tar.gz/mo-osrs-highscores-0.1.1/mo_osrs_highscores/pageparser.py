import requests

from .Exceptions import NameNotFoundException
from .resources.ballsandpenis import BallsAndPenis
from bs4 import BeautifulSoup

class ParsePage:

    @staticmethod
    def __check_page_for_error(soup, playerName):
        listResult = soup.find_all('i')
        if "does not feature in the" in listResult[0].text.strip():
            raise NameNotFoundException("{} was not found on hiscores".format(playerName))

    @staticmethod
    def request_page(playerName):
        form_data = {"user1": playerName, "user2": "large_unit", "submit":"Compare"}

        data = requests.post("https://secure.runescape.com/m=hiscore_oldschool/compare", data=form_data)
        checkData = BeautifulSoup(data.content)
        try:
            ParsePage.__check_page_for_error(checkData, playerName)
        except NameNotFoundException:
            raise NameNotFoundException("{} was not found on hiscores".format(playerName))

        table1 = checkData.find("div", {"class":"widescroll-content"})
        table = table1.find("table")
        tableRows = table.find_all("tr")

        SkillFlag = True
        MinigameFlag = False




        for row in tableRows:
            attributes = row.find_all("td")

            if(SkillFlag):
                if(attributes[1].text.strip() == "Construction"):
                    SkillFlag = False
                    MinigameFlag = True
                name = attributes[1].text.strip()

                rankString = attributes[2].text.strip().replace(',','')
                rank = rankString if rankString.isnumeric() else -1
                levelString = attributes[3].text.strip().replace(',','')
                level = levelString if levelString.isnumeric() else -1
                xpString = attributes[4].text.strip().replace(',','')
                xp = xpString if xpString.isnumeric() else -1
                BallsAndPenis.add_skill(name, rank, level, xp)
            elif(MinigameFlag):
                if(attributes[1].text.strip() == "Rifts closed"):
                    MinigameFlag = False

                name = attributes[1].text.strip()
                rankString = attributes[2].text.strip().replace(',','')
                rank = rankString if rankString.isnumeric() else -1
                scoreString = attributes[4].text.strip().replace(',','')
                score = scoreString if scoreString.isnumeric() else -1
                BallsAndPenis.add_minigame(name, rank, score)
            else:

                name = attributes[1].text.strip()
                rankString = attributes[2].text.strip().replace(',','')
                rank = rankString if rankString.isnumeric() else -1
                killString = attributes[4].text.strip().replace(',','')
                kill = killString if killString.isnumeric() else -1
                BallsAndPenis.add_boss(name, rank, kill)

        del BallsAndPenis.Skills["Rank"]
        del BallsAndPenis.Skills[""]
        del BallsAndPenis.MiniGames["Rank"]






