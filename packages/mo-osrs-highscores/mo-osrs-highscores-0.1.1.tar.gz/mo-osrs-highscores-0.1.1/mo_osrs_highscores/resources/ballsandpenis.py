class BallsAndPenis:
    Skills = {}
    MiniGames = {}
    Boss = {}
    HighScores = {}



    @staticmethod
    def add_skill(skillName, skillRank, skillLevel, xp):
        BallsAndPenis.Skills[skillName] = {
            "Rank": skillRank,
            "Level": skillLevel,
            "Xp": xp
        }

    @staticmethod
    def add_minigame(miniName, miniRank, miniScore):
        BallsAndPenis.MiniGames[miniName] = {
            "Rank": miniRank,
            "Score": miniScore
        }

    @staticmethod
    def add_boss(bossName, bossRank, bossKill):
        BallsAndPenis.Boss[bossName] = {
            "Rank": bossRank,
            "Kills": bossKill
        }

    @staticmethod
    def getMegaDic():
        BallsAndPenis.HighScores = {
            "Skills": BallsAndPenis.Skills,
            "MiniGames": BallsAndPenis.MiniGames,
            "Bosses": BallsAndPenis.Boss
        }
