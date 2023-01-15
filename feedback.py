class Feedback:
    """
    A class used to represent a user's feedback

    Attributes
    ----------
    title : str
        the name of the user's favorite anime
    ranking_score : int
        a user's preference towards a ranking algorithm
    synopsis_score : int
        a user's preference towards a synopsis algorithm
    item_based_score : int
        a user's preference towards an item_based algorithm

    Methods
    --------
    weighted_scores()
        weighs the users personalied scores

    get_fb_title()
        returns the user's favorite anime

    get_fb_ranking_score()
        returns the user's preference towards ranking algorithm

    get_fb_synopsis_score()
        returns the user's preference towards synopsis algorithm

    get_fb_item_based_score()
        returns the user's preference towards item_base algorithm

    """
    def __init__(self, title, ranking_score, synopsis_score, item_based_score):
        self.title = title
        self.ranking_score = ranking_score
        self.synopsis_score = synopsis_score
        self.item_based_score = item_based_score

    def weighted_scores(self):
        """
        weights the user rankings
        :param:
        :return:
        """
        sum = self.ranking_score + self.synopsis_score + self.item_based_score
        self.ranking_score = int(self.ranking_score / sum * 10)
        self.synopsis_score = int(self.synopsis_score / sum * 10)
        self.item_based_score = 10 - self.ranking_score - self.synopsis_score

    def __repr__(self):
        return f'Feedback({self.title}, {self.ranking_score}, {self.synopsis_score}, {self.item_based_score})'

    def get_fb_title(self):
        return self.title

    def get_fb_ranking_score(self):
        return self.ranking_score

    def get_fb_synopsis_score(self):
        return self.synopsis_score

    def get_fb_item_based_score(self):
        return self.item_based_score
