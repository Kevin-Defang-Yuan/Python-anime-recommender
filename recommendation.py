class Recommendation:
    """
    A class used to store recommendations generated

    Attributes
    ----------
    rec_list : list[str]
        a list that contains names of titles

    Methods
    --------
    append_rec_list(list_recommendations)
        allows other classes to append titles to the rec_list attribute of a recommendation object

    get_rec_list()
        returns attribute rec_list
    """
    def __init__(self):
        self.rec_list = []

    def get_rec_list(self):
        return self.rec_list

    def append_rec_list(self, list_recommendations):
        """
        adds titles to a recommendation object
        :param list_recommendations: a list of recommendations
        :return:
        """
        for title in list_recommendations:
            self.rec_list.append(title)

    def __repr__(self):
        output = ''
        for title in self.rec_list:
            output += f'{title}\n'
        return output
