import zmq
import pandas as pd
import numpy as np
import random
import json
import time

# starts the zeromq server based off of suggestion from zeromq.org
def start_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)  #
    socket.bind("tcp://*:5556")  # bind to port 5556
    # Load the dataset
    dataset = pd.read_csv('./imbd_videogame_reviews.csv')    # name of csv

    while True:
        # Wait for the next request from the client
        message = socket.recv_json()
        print("Received request: %s" % message)

        # Get random game based on constraints
        response = get_random_game(dataset, message)

        # Send reply back to the client
        socket.send_json(response)

        # Sleep for 1 second
        time.sleep(1)


# gets a random game from the data set based off of the constraints
def get_random_game(dataset, constraints):
    filtered_dataset = dataset
    if constraints.get('genres', ''):
        filtered_dataset = filtered_dataset[filtered_dataset['genres'].str.contains(constraints['genres'])]
    if constraints.get('startYear', ''):
        filtered_dataset = filtered_dataset[filtered_dataset['startYear'] == int(constraints['startYear'])]
    if constraints.get('averageRating', 0):
        filtered_dataset = filtered_dataset[filtered_dataset['averageRating'] >= float(constraints['averageRating'])]
    if constraints.get('numVotes', 0):
        filtered_dataset = filtered_dataset[filtered_dataset['numVotes'] >= int(constraints['numVotes'])]
    if 'isAdult' in constraints:
        filtered_dataset = filtered_dataset[filtered_dataset['isAdult'] == int(constraints['isAdult'])]

    # Convert Pandas/Numpy types to native Python types, had to look up how to do this online 
    def convert_types(game):
        for key, value in game.items():
            if isinstance(value, np.int64):
                game[key] = int(value)
            elif isinstance(value, np.float64):
                game[key] = float(value)
            elif pd.isna(value):
                game[key] = None  # Convert NaNs to None
        return game

    # If no game matches exactly, suggest a game based on genre and closest average rating
    #
    # example used: if genre, startyear, averagerating, numvotes, isadult does not match, it takes the genre and average rating and finds the next 
    # game using averagerating that fits it
    # ex search : genre horror, averagerating 7.0
    # suggested return: genre horror, averagerating 7.1, title: xxxxxx zombies xxxxxx
    # the return makes sure that the genre and rating are similar by taking account same genre, then next closest rating 
    if filtered_dataset.empty:
        closest_game = None
        min_rating_diff = float('inf')  # Initialize with a large number

        if constraints.get('genres', ''):
            suggestion_dataset = dataset[dataset['genres'].str.contains(constraints['genres'])]

            # Find the game with the closest average rating to the specified value
            for _, row in suggestion_dataset.iterrows():
                rating_diff = abs(row['averageRating'] - float(constraints.get('averageRating', 0)))
                if rating_diff < min_rating_diff:
                    min_rating_diff = rating_diff
                    closest_game = row

        if closest_game is not None:
            return convert_types({
                'primaryTitle': closest_game['primaryTitle'],
                'genres': closest_game['genres'],
                'startYear': closest_game['startYear'],
                'averageRating': closest_game['averageRating'],
                'numVotes': closest_game['numVotes'],
                'isAdult': closest_game['isAdult']
            })
        else:
            return {'error': 'No games found matching criteria'}

    random_game = filtered_dataset.sample(n=1).iloc[0]      # had to look up iloc and Pandas and understand how to use
    return convert_types({
        'primaryTitle': random_game['primaryTitle'],
        'genres': random_game['genres'],
        'startYear': random_game['startYear'],
        'averageRating': random_game['averageRating'],
        'numVotes': random_game['numVotes'],
        'isAdult': random_game['isAdult']
    })

if __name__ == "__main__":
    start_server()