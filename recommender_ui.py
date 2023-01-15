import feedback as fb
import recommendation as rec
import database as d
import ranking_generator as rg
import synopsis_generator as sg
import item_based_generator as ibg

"""
This is the main file that is called in the command prompt
Does simple input/output
"""

#Initialize database to help validate user input
anime_database = d.Database()

options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
while True:
    ranking = int(input('On a scale of 1-10, how much would you like to get recommended titles that are most highly rated among the community?'))
    if ranking not in options:
        print('Please enter a number between 1 and 10')
        continue
    else:
        break

while True:
    title = input('What is your favorite anime?')
    if anime_database.check_title_exists(title) == False:
        print('That title does not exist, try again')
        continue
    else:
        break

while True:
    synopsis = int(input('On a scale of 1-10, how much would you like to get recommended titles that have similar plots to your favorite anime?'))
    if synopsis not in options:
        print('Please enter a number between 1 and 10')
        continue
    else:
        break

while True:
    item_based = int(input('On a scale of 1-10, how much would you like to get recommended titles based on opinions of other users who also liked your favorite anime?'))
    if item_based not in options:
        print('Please enter a number between 1 and 10')
        continue
    else:
        break

#Create instance of user feedback
user_preference = fb.Feedback(title, ranking, synopsis, item_based)

#Weigh the scores
user_preference.weighted_scores()

#Create instance of user recommendation
output = rec.Recommendation()

#Run the ranking recommender
ranking_algorithm = rg.Ranking_generator()
output.append_rec_list(ranking_algorithm.generate_ranking(user_preference))

#Run the synopsis recommender
synopsis_algorithm = sg.Synopsis_generator()
output.append_rec_list(synopsis_algorithm.generate_ranking(user_preference))

#Run the item_based recommender
item_based_algorithm = ibg.Item_based_generator()
output.append_rec_list(item_based_algorithm.generate_ranking(user_preference))

#Print recommendations
print('Here are your recommendations:')
print(repr(output))
