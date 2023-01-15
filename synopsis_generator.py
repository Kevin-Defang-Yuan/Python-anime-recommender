import database as d
import feedback as fb
import recommendation as rec
import pandas as pd

class Synopsis_generator():
    """
    Machine that generates content-based recommedations based on synopsis

    Attributes
    ----------
    database_access : Database()
        contains Database object to get data from

    anime_data : dataframe
        contains dataframe of anime.csv

    synopsis_data : dataframe
        contains dataframe of anime_with_synopsis.csv

    cosine_sim : matrix
        matrix of cosine similarity between all titles

    rec_list : Recommendation()
        contains a Recommendation object to append results

    Methods
    ---------
    generate_ranking(fb)
        generates top-N recommendations
        appends recommendations to Recommendation object
        return Recommendation object

    """
    def __init__(self):
        self.database_access = d.Database()
        self.database_access.load_anime_data()
        self.database_access.load_synopsis_data()
        self.database_access.load_cosine_sim()
        self.anime_data = self.database_access.get_anime_data()
        self.synopsis_data = self.database_access.get_synopsis_data()
        self.cosine_sim = self.database_access.get_cosine_sim()
        self.rec_list = rec.Recommendation()

    def generate_ranking(self, fb):
        """
        generates synopsis top-N recommendations
        code inspired from source: https://www.datacamp.com/tutorial/recommender-systems-python
        :param fb: feedback object
        :returns list_of_rec: list of recommendations
        """
        synopsis_weight = fb.get_fb_synopsis_score()
        title = fb.get_fb_title()

        #Map anime_id to anime name
        indices = pd.Series(self.synopsis_data.index, index=self.synopsis_data['Name']).drop_duplicates()
        title_index = indices[title]

        #get the cosine similarity scores for queried anime
        sim_scores = list(enumerate(self.cosine_sim[title_index]))

        #sort the list so that most similar appears first
        sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse=True)

        #starts at 1 because we do not include the anime itself, since
        #an anime is always most similar to itself
        sim_scores = sim_scores[1:synopsis_weight+1]

        #find indices of anime recommendations
        anime_indices = [i[0] for i in sim_scores]

        #appends anime names to Recommendation object and returns
        list_of_rec = []
        for i in anime_indices:
            list_of_rec.append(str(self.synopsis_data.iloc[i][1]))
        return list_of_rec
