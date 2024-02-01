#
import json
import glob
def return_Top_anime(nr):
   # open ./data/top_anime_list2.json
   with open('./data/top_anime_list2.json') as json_file:
      json_file = json.load(json_file)
   
   # return the top nr animes
   return json_file[:nr]

message = {"type": "sucess", "results": return_Top_anime(10)}
# print(json.dumps(message))


def return_age_rating(rating):
   # open ./data/{rating}_*.json
   with open(f'./data/age_rating_list{rating}.json') as json_file:
      json_file = json.load(json_file)
   
   return json_file

message = {"type": "sucess", "results": return_age_rating("teens")}

# print(json.dumps(message))

from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np

import numpy as np

def create_genre_pie_chart(source_type=None):
    # open the ./data/Genres_Sources.json file
    with open('./data/Genres_Sources.json') as f:
        data = json.load(f)

    # filter the data by source type if specified
    if source_type:
        data = [item for item in data if item.get('Source') == source_type]

    # create a dictionary to store the count of each genre
    genre_count = {}

    # iterate over each item and count the number of occurrences of each genre
    for item in data:
        genres_str = item.get('Genres', '')
        genres = genres_str.split(',')
        for genre in genres:
            genre = genre.strip()
            if genre:
                if genre in genre_count:
                    genre_count[genre] += 1
                else:
                    genre_count[genre] = 1

    # create a list of genre labels and a list of corresponding counts
    labels = list(genre_count.keys())
    counts = list(genre_count.values())

    # percentages smaller than 5% will be combined into the "Other" category
    threshold = 0.05
    counts_array = np.array(counts)
    mask = counts_array / counts_array.sum() < threshold
    counts_array[mask] = 0
    other_count = counts_array.sum()
    other_label = 'Other'

    # replace small genres with 'Other'
    labels = np.array(labels)
    labels[mask] = other_label

    # create a list of genre labels and a list of corresponding counts after replacement
    labels, counts = np.unique(labels, return_counts=True)
    
    # remove "Other" if it has no entries
    if other_label in labels and counts[list(labels).index(other_label)] == 0:
        counts = counts[labels != other_label]
        labels = labels[labels != other_label]
    
    # append the other count to the "Other" category
    if other_count > 0:
        counts = np.append(counts, other_count)
    
    # create a pie chart
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(counts, labels=labels, startangle=90, autopct='%1.1f%%')
    ax.axis('equal')
    title = 'Pie Chart of Genres'
    if source_type:
        title += f' for {source_type}'
    ax.set_title(title)

    # move the pie chart to the right to make space for the legend
    ax.legend(wedges, labels, title="Genres", loc="center left", bbox_to_anchor=(0.85, 0, 0.5, 1))

    ax.axis('equal')
    ax.set_title(f'Pie Chart of Genres for Source: {source_type}')
    plt.savefig(f'./data/{source_type}_pie_chart.png')

        
# return_airing("currently_airing")
# return_airing("not_yet_aired")
# return_airing("finished_airing")


create_genre_pie_chart("Original")
create_genre_pie_chart("Light novel")
create_genre_pie_chart("Visual novel")
create_genre_pie_chart("Novel")
create_genre_pie_chart("4-koma manga")
create_genre_pie_chart("Web manga")
create_genre_pie_chart("Web novel")
create_genre_pie_chart("Game")
create_genre_pie_chart("Music")
create_genre_pie_chart("Book")
create_genre_pie_chart("Other")
create_genre_pie_chart("Unknown")
create_genre_pie_chart("Picture book")
create_genre_pie_chart("Mixed media")
create_genre_pie_chart("Manga")

#All Sources:
#['Manga' 'Visual novel' 'Novel' '4-koma manga' 'Original' 'Light novel'
# 'Web manga' 'Web novel' 'Game' 'Music' 'Book' 'Other' 'Unknown'
# 'Picture book' 'Mixed media' 'Card game' 'Radio']


def return_airing(status):
    # get all files in ./data/ directory that match the pattern "{status}_*.json"
    file_paths = glob.glob(f"./data/{status}_*.json")
    
    # create an empty list to store all the data from the files
    
    # iterate over each file and load its contents as JSON
    for file_path in file_paths:
        with open(file_path) as f:
            json_data = json.load(f)
            
    # return the list of all JSON data
    return json_data


message = {"type": "sucess", "results": return_airing("finished_airing")}
print(json.dumps(message))
      
