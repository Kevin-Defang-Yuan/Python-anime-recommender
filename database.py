import pandas as pd
import os.path as os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from scipy import sparse
from scipy.sparse import csr_matrix
import numpy as np

class Database:
    """
    A class used to store and prepare data before given to algorithms
    All the dataset are from link: https://www.kaggle.com/datasets/hernan4444/anime-recommendation-database-2020?select=animelist.csv

    Three datasets were used from this link:
    1. anime.csv
    2. anime_with_synopsis.csv
    3. animelist.csv

    Attributes
    ----------
    anime_data : pandas dataframe
        dataframe of anime.csv

    synopsis_data : pandas datarame
        dataframe of anime_with_synopsis.csv

    cosine_sim : similarity matrix
        cosine similarity of all anime with each other from TF-IDF scores
        used for synopsis_recommender

    rating_data : pandas dataframe
        dataframe of animelist.csv

    anime_pivot_table : pivot table
        pivot table of rating_data

    anime_pivot_table_matrix : matrix
        matrix of anime_pivot_table

    Methods
    --------
    read_data(file_name)
        reads csv files into pandas dataframe

    check_file_exists(file_name)
        checks if a file exists in the working directory

    check_title_exists(title)
        checks if an anime title exists in anime.csv

    transformed_anime_data()
        reads in anime.csv and saves it into a dataframe
        creates a new column for weighted scores and calculates the scores
        returns the dataframe

    load_anime_data()
        sets Database attribute anime_data to
        dataframe returned from transformed_anime_data()

    get_anime_data()
        returns anime_data attribute

    transformed_synopsis_data()
        reads in anime_with_synopsis.csv and saves it into dataframe
        returns the dataframe

    load_synopsis_data()
        sets Database attribute synopsis_data to
        dataframe returned from transformed_synopsis_data()

    get_synopsis_data()
        returns synopsis_data attribute

    create_tfidf_matrix()
        creates a tfidf matrix, called cosine_sim, that is used for synopsis_recommender

    load_cosine_sim()
        sets Database attribute cosine_sim to
        matrix returned from create_tfidf_matrix()

    get_cosine_sim()
        returns cosine_sim attribute

    transformed_item_based_data()
        reads in animelist.csv and saves it into dataframe
        filters out the dataframe to reduce size
        merges dataframe with anime.csv so that anime_id maps to anime name
        if the dataframe isn't saved in working directory, then save it as rating_data.csv
        returns the dataframe

    load_rating_data()
        sets Database attribute rating_data to
        dataframe returned from transformed_item_based_data()

    get_rating_data()
        returns rating_data attribute

    """
    def __init__(self):
        self.anime_data = None
        self.synopsis_data = None
        self.cosine_sim = None
        self.rating_data = None

    def read_data(self, file_name):
        return pd.read_csv(file_name)

    def check_file_exists(self, file_name):
        return os.exists(file_name)

    def get_anime_data(self):
        return self.anime_data

    def load_anime_data(self):
        self.anime_data = self.transformed_anime_data()

    def transformed_anime_data(self):
        """
        Modifys the anime data and makes it readable for ranking algorithm
        Code inspired from source: https://www.datacamp.com/tutorial/recommender-systems-python
        :param:
        :return anime_data: modified anime dataframe from anime.csv
        """
        anime_data = self.read_data('anime.csv')
        anime_data['Score'] = pd.to_numeric(anime_data['Score'], errors='coerce')

        #consolidates all the scores to get total number of scores
        for x in range(1,11):
            number = 'Score-' + str(x)
            anime_data[number] = pd.to_numeric(anime_data[number],errors='coerce')
        anime_data['Scored_by'] = (anime_data['Score-10'] +
                                anime_data['Score-9'] +
                                anime_data['Score-8'] +
                                anime_data['Score-7'] +
                                anime_data['Score-6'] +
                                anime_data['Score-5'] +
                                anime_data['Score-4'] +
                                anime_data['Score-3'] +
                                anime_data['Score-2'] +
                                anime_data['Score-1'])
        #Create new column Wscore: weighted score
        #Calculate mean rating of all anime
        C = anime_data['Score'].mean()
        #Calculates minimum number of votes required to be in the chart
        m = anime_data['Scored_by'].quantile(0.8)

        """
        Calculates weighted ratings
        Code inspired from source: https://www.datacamp.com/tutorial/recommender-systems-python
        :param x: score
        :param m: min number of votes to be in 80% percentile
        :param C: mean score of all anime
        :return: returns weighted score
        """
        def weighted_rating(x, m=m, C=C):
            v = x['Scored_by']
            R = x['Score']
            return (v/(v+m) * R) + (m/(m+v) * C)
        anime_data['Wscore'] = anime_data.apply(weighted_rating, axis=1)

        #drop all rows where number of ratings is below 50th quantile.
        drop_index_names = anime_data[ anime_data['Scored_by'] <  anime_data['Scored_by'].mean()].index
        anime_data.drop(drop_index_names, inplace=True)
        return anime_data

    def transformed_synopsis_data(self):
        """
        Prepares the data for synopsis recommender
        Code inspired from source: https://www.datacamp.com/tutorial/recommender-systems-python
        :param:
        :returns synopsis_data: modified dataframe from anime_with_synopsis.csv
        """
        synopsis_data = self.read_data('anime_with_synopsis.csv')
        synopsis_data = synopsis_data.rename(columns={'sypnopsis': 'synopsis'})
        synopsis_data['synopsis'] = synopsis_data['synopsis'].fillna('')
        return synopsis_data

    def load_synopsis_data(self):
        self.synopsis_data = self.transformed_synopsis_data()

    def get_synopsis_data(self):
        return self.synopsis_data

    def create_tfidf_matrix(self):
        """
        Creates tfidf matrix for synopsis recommender
        Code inspired from source: https://www.datacamp.com/tutorial/recommender-systems-python
        :param:
        :returns cosine_sim: a matrix of all anime similarities with all other anime
        """
        #remove all stop words
        tfidf = TfidfVectorizer(stop_words='english')
        #apply tfidf to synopsis
        tfidf_matrix = tfidf.fit_transform(self.synopsis_data['synopsis'])
        #generate cosine similarities between all animes
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        return cosine_sim

    def load_cosine_sim(self):
        self.cosine_sim = self.create_tfidf_matrix()

    def get_cosine_sim(self):
        return self.cosine_sim

    def get_synopsis_data(self):
        return self.synopsis_data

    def load_rating_data(self):
        #If file doesn't exist, then we need to read original csv file
        if (self.check_file_exists('rating_data.csv') == False):
            self.rating_data = self.transformed_item_based_data()
        else:
            self.rating_data = self.read_data('rating_data.csv')

    def get_rating_data(self):
        return self.rating_data

    def transformed_item_based_data(self):
        """
        modifys dataframe for item_based recommender
        code inspired from source: https://everydaycodings.medium.com/anime-recommendation-system-collaborative-method-ca3e84ee41a0
        :param:
        :returns rating_data: modified dataframe of animelist.csv
        """
        rating_data = self.read_data('animelist.csv')
        anime_data = self.read_data('anime.csv')
        anime_data = anime_data.rename(columns={'MAL_ID': 'anime_id'})

        user_counts = rating_data['user_id'].value_counts()
        anime_counts = rating_data['anime_id'].value_counts()

        #remove all users who have less than 500 votes
        rating_data = rating_data[rating_data['user_id'].isin(user_counts[user_counts >= 500].index)]

        #removes all anime that have less than 20000 votes
        rating_data = rating_data[rating_data['anime_id'].isin(anime_counts[anime_counts >= 20000].index)]

        #merge rating_data with anime_data based on anime_id to map anime_id with anime name
        anime_contact_data = anime_data[['anime_id', 'Name']]
        rating_data = rating_data.merge(anime_contact_data, left_on='anime_id', right_on='anime_id', how='left')
        rating_data = rating_data[['user_id', 'Name', 'anime_id', 'rating']]

        #Save filtered data so we do not need to read full data every time
        if (self.check_file_exists('rating_data.csv') == False):
            rating_data.to_csv('rating_data.csv')

        return rating_data

    def check_title_exists(self, title):
        """
        Checks anime.csv to see if a particular title exists in the dataframe
        :param title: anime title that user inputs
        :returns boolean:
        """
        anime_data = self.read_data('anime.csv')
        valid_anime_names = anime_data['Name'].tolist()
        return (title in valid_anime_names)
