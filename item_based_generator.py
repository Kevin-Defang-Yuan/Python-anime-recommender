import database as d
import feedback as fb
import recommendation as rec
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy import sparse
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

class Item_based_generator():
    """
    Machine that generates item-based recommendations

    Attributes
    ----------
    database_access : Database()
        Has a Database object to obtain data from
    rating_data : dataframe
        Stores rating_data from Database

    Methods
    --------
    generate_ranking(fb)
        returns top-N recommendations

    """
    def __init__(self):
        self.database_access = d.Database()
        self.database_access.load_rating_data()
        self.rating_data = self.database_access.get_rating_data()

    def generate_ranking(self, fb):
        """
        generates item_based top-N recommendations
        code inspired from source: https://everydaycodings.medium.com/anime-recommendation-system-collaborative-method-ca3e84ee41a0
        :param fb: feedback object
        :return list_of_rec: a list of recommendations
        """
        item_based_weight = fb.get_fb_item_based_score()
        title = fb.get_fb_title()
        #creates pivot table: each anime and the respective ratings by users
        anime_pivot_table = self.rating_data.pivot_table(index="Name", columns="user_id", values="rating").fillna(0)

        #converts pivot table into a matrix and condenses matrix to save space
        anime_pivot_table_matrix = csr_matrix(anime_pivot_table.values)

        #find closest neighbors to queried anime
        model = NearestNeighbors(metric="cosine", algorithm="brute")
        model.fit(anime_pivot_table_matrix)

        #locate the anime_id of a given anime based on name
        anime_title_index = None
        for i in range(anime_pivot_table.shape[0]):
            if anime_pivot_table.index[i] == title:
                anime_title_index = i
        query = anime_pivot_table.iloc[anime_title_index, :].values.reshape(1, -1)

        #generate recommendations
        distance, suggestions = model.kneighbors(query, n_neighbors=item_based_weight+1)

        #append recommendations to a Recommendation object
        list_of_rec = []
        for i in range(1, len(distance.flatten())):
            list_of_rec.append(str(anime_pivot_table.index[suggestions.flatten()[i]]))
        return list_of_rec
