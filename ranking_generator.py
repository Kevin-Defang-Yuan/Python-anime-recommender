import database as d
import feedback as fb
import recommendation as rec
import pandas as pd

class Ranking_generator():
    """
    A machine that generates ranking recommendations based on weighted score

    Attributes
    ----------
    database_access : Database()
        stores a Database object so it can access data from it

    anime_data : dataframe
        stores dataframe of anime.csv

    Methods
    -------
    generate_ranking(fb)
        returns top-N ranking recommendations
    """
    def __init__(self):
        self.database_access = d.Database()
        self.database_access.load_anime_data()
        self.anime_data = self.database_access.get_anime_data()
        #self.rec_list = rec.Recommendation()

    def generate_ranking(self, fb):
        """
        generates top-N ranking recommendations
        Code inspired from source: https://www.datacamp.com/tutorial/recommender-systems-python
        :param fb: feedback object
        :returns list_of_rec: list of recommendations
        """
        ranking_weight = fb.get_fb_ranking_score()

        #Sorts dataframe by weighted score
        self.anime_data = self.anime_data.sort_values('Wscore', ascending=False)

        #appends anime names to Recommendation object
        list_of_rec = []
        for i in range(ranking_weight):
            list_of_rec.append(str(self.anime_data.iloc(0)[i][1]))
        return list_of_rec
