# Need to put in your own api key

# I chose to only do this previous season of 2024 because the player differences like 
# Saquon Barkley on the eagles completely changes the teams, 
# so while the data is less than someone who has used many years, 
# I feel as though is is more accurate to these teams specifically

# Three features: (I was kind of confused what the three feature requirements meant)
#   1. API stats
#   2. Generate data from jsons to csvs automatically
#   3. Linear regression model

import requests
import json
import os
import csv
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# iterate through links to get data from each api
links = ["https://nfl-api-data.p.rapidapi.com/nfl-team-statistics", "https://nfl-api-data.p.rapidapi.com/nfl-team-schedule", "https://nfl-api-data.p.rapidapi.com/nfl-scoreboard"]

# id 12 is chiefs and id 21 is eagles
for link in links:
    if link == "https://nfl-api-data.p.rapidapi.com/nfl-team-statistics":
        if not os.path.exists("NFL\\cheifs-team-stats.json"):
            print("Downloading data from API...") # debugging
            querystring = {"id":"12","year":"2024"}

            headers = {
                "x-rapidapi-key": "",
                "x-rapidapi-host": "nfl-api-data.p.rapidapi.com"
            }

            response = requests.get(link, headers=headers, params=querystring)

            local_filename = "NFL\\cheifs-team-stats.json"

            if response.status_code == 200:
                with open(local_filename, 'w') as f:
                    json.dump(response.json(), f, indent=4)
                print(f"Data saved to '{local_filename}'") # debugging
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}") # debugging
        if not os.path.exists("NFL\\eagles-team-stats.json"):
            print("Downloading data from API...") # debugging
            querystring = {"id":"21","year":"2024"}

            headers = {
                "x-rapidapi-key": "",
                "x-rapidapi-host": "nfl-api-data.p.rapidapi.com"
            }

            response = requests.get(link, headers=headers, params=querystring)

            local_filename = "NFL\\eagles-team-stats.json"

            if response.status_code == 200:
                with open(local_filename, 'w') as f:
                    json.dump(response.json(), f, indent=4)
                print(f"Data saved to '{local_filename}'") # debugging
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}") # debugging
        if not os.path.exists("NFL\\cheifs-team-stats.csv"):
            json_file_path = 'NFL\\cheifs-team-stats.json'

            with open(json_file_path, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)

            rows = []

            # Loop through categories and stats to organize them into rows
            for category in data['statistics']['splits']['categories']:
                for stat in category['stats']:
                    # Collect name and value
                    rows.append([stat.get('name', ''), stat.get('value', '')])

            # Make csv
            with open('NFL\\cheifs-team-stats.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                # Write the header row
                writer.writerow(['name', 'value'])

                # Write the stat values
                for row in rows:
                    writer.writerow(row)

            print("CSV file has been written successfully.")
        if not os.path.exists("NFL\\eagles-team-stats.csv"):
            json_file_path = 'NFL\\eagles-team-stats.json'

            with open(json_file_path, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)

            rows = []

            # Loop through categories and stats to organize them into rows
            for category in data['statistics']['splits']['categories']:
                for stat in category['stats']:
                    # Collect name and value
                    rows.append([stat.get('name', ''), stat.get('value', '')])

            # Make csv
            with open('NFL\\eagles-team-stats.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                # Write the header row
                writer.writerow(['name', 'value'])

                # Write the stat values
                for row in rows:
                    writer.writerow(row)

            print("CSV file has been written successfully.")
    elif link == "https://nfl-api-data.p.rapidapi.com/nfl-team-schedule":
        if not os.path.exists("NFL\\cheifs-team-schedule.json"):
            print("Downloading data from API...") # debugging
            querystring = {"id":"12"}

            headers = {
                "x-rapidapi-key": "",
                "x-rapidapi-host": "nfl-api-data.p.rapidapi.com"
            }

            response = requests.get(link, headers=headers, params=querystring)

            local_filename = "NFL\\cheifs-team-schedule.json"

            if response.status_code == 200:
                with open(local_filename, 'w') as f:
                    json.dump(response.json(), f, indent=4)
                print(f"Data saved to '{local_filename}'") # debugging
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}") # debugging
        if not os.path.exists("NFL\\eagles-team-schedule.json"):
            print("Downloading data from API...") # debugging
            querystring = {"id":"21"}

            headers = {
                "x-rapidapi-key": "",
                "x-rapidapi-host": "nfl-api-data.p.rapidapi.com"
            }

            response = requests.get(link, headers=headers, params=querystring)

            local_filename = "NFL\\eagles-team-schedule.json"

            if response.status_code == 200:
                with open(local_filename, 'w') as f:
                    json.dump(response.json(), f, indent=4)
                print(f"Data saved to '{local_filename}'") # debugging
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}") # debugging
    elif link == "https://nfl-api-data.p.rapidapi.com/nfl-scoreboard":
        if not os.path.exists("NFL\\2024-scoreboard.json"):
            querystring = {"year":"2024"}

            headers = {
                "x-rapidapi-key": "",
                "x-rapidapi-host": "nfl-api-data.p.rapidapi.com"
            }

            response = requests.get(link, headers=headers, params=querystring)

            local_filename = "NFL\\2024-scoreboard.json"

            if response.status_code == 200:
                with open(local_filename, 'w') as f:
                    json.dump(response.json(), f, indent=4)
                print(f"Data saved to '{local_filename}'") # debugging
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}") # debugging
    else:
        print("Passing")

# Figuring out how to parse the data from the scoreboard json took a lot of trial and error and with the help of AI

# Create csv for game scores for each team
if not os.path.exists("NFL\\chiefs-games_scores.json"):

    # Load the JSON
    with open('NFL\\2024-scoreboard.json', 'r') as file:
        data = json.load(file)

    # Open a CSV
    with open('NFL\\chiefs-games_scores.csv', 'w', newline='') as csvfile:
        fieldnames = ['game', 'chiefs_score', 'opponent_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()  # Write the header row
        
        game_counter = 1  # Start counting games from 1
        
        # Iterating through events
        for event in data['events']:
            # Iterating through each competition
            for competition in event['competitions']:
                # Initialize scores
                chiefs_score = None
                opponent_score = None
                
                # Iterate through competitors in the competition
                for competitor in competition['competitors']:
                    # If the competitor is chiefs
                    if competitor['id'] == '12':
                        chiefs_score = competitor['score']
                    else:
                        opponent_score = competitor['score']
                
                # If we found scores for both competitors, write to CSV
                if chiefs_score is not None and opponent_score is not None:
                    writer.writerow({
                        'game': game_counter,
                        'chiefs_score': chiefs_score,
                        'opponent_score': opponent_score
                    })
                    game_counter += 1  # Increment the game counter

if not os.path.exists("NFL\\eagles-games_scores.json"):

    # Load the JSON
    with open('NFL\\2024-scoreboard.json', 'r') as file:
        data = json.load(file)

    # Open a CSV 
    with open('NFL\\eagles-games_scores.csv', 'w', newline='') as csvfile:
        fieldnames = ['game', 'eagles_score', 'opponent_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()  # Write the header row
        
        game_counter = 1  # Start counting games from 1
        
        # Iterating through events
        for event in data['events']:
            # Iterating through each competition
            for competition in event['competitions']:
                # Initialize scores
                eagles_score = None
                opponent_score = None
                
                # Iterate through competitors in the competition
                for competitor in competition['competitors']:
                    # If the competitor is eagles
                    if competitor['id'] == '21':
                        eagles_score = competitor['score']
                    else:
                        opponent_score = competitor['score']
                
                # If we found scores for both competitors, write to CSV
                if eagles_score is not None and opponent_score is not None:
                    writer.writerow({
                        'game': game_counter,
                        'eagles_score': eagles_score,
                        'opponent_score': opponent_score
                    })
                    game_counter += 1  # Increment the game counter

# Create csv for both chiefs and eagles for overall stats to compare for regression
if not os.path.exists("NFL\\eagles_combined_game_scores.json") and not os.path.exists("NFL\\chiefs_combined_game_scores.json"):

    # Load team stats for the Chiefs
    chiefs_stats = {}
    with open('NFL\\cheifs-team-stats.csv', 'r') as stats_file:
        reader = csv.reader(stats_file)
        next(reader)  # Skip header
        for row in reader:
            stat_name, stat_value = row
            chiefs_stats[stat_name] = stat_value

    # Load team stats for the Eagles
    eagles_stats = {}
    with open('NFL\\eagles-team-stats.csv', 'r') as stats_file:
        reader = csv.reader(stats_file)
        next(reader)  # Skip header
        for row in reader:
            stat_name, stat_value = row
            eagles_stats[stat_name] = stat_value

    # Load game scores for the Chiefs
    chiefs_game_scores = []
    with open('NFL\\chiefs-games_scores.csv', 'r') as scores_file:
        reader = csv.DictReader(scores_file)
        for row in reader:
            chiefs_game_scores.append(row)

    # Load game scores for the Eagles
    eagles_game_scores = []
    with open('NFL\\eagles-games_scores.csv', 'r') as scores_file:
        reader = csv.DictReader(scores_file)
        for row in reader:
            eagles_game_scores.append(row)

    # Function to write the combined CSV for a specific team
    def write_combined_csv(team_name, game_scores, team_stats, file_name):
        with open(file_name, 'w', newline='') as combined_file:
            fieldnames = ['game', f'{team_name}_score', f'{team_name}_opponent_score'] + list(team_stats.keys())
            writer = csv.DictWriter(combined_file, fieldnames=fieldnames)
            
            writer.writeheader()  # Write the header row

            score_name = f'{team_name}_score'
            
            # Iterate through each game for the team
            for idx, game in enumerate(game_scores, 1):
                # Create a row with game details and stats for the team
                row = {
                    'game': idx,
                    f'{team_name}_score': game[score_name],  # This is a placeholder for the team score
                    f'{team_name}_opponent_score': game['opponent_score']
                }
                
                # Add stats to the row
                for stat_name, stat_value in team_stats.items():
                    row[stat_name] = stat_value
                
                # Write the row to the CSV
                writer.writerow(row)

    # Write the combined CSV for Chiefs
    write_combined_csv('chiefs', chiefs_game_scores, chiefs_stats, 'NFL\\chiefs_combined_game_stats.csv')

    # Write the combined CSV for Eagles
    write_combined_csv('eagles', eagles_game_scores, eagles_stats, 'NFL\\eagles_combined_game_stats.csv')

print("All data downloaded")

# Load the data
chiefs_df = pd.read_csv('NFL\\chiefs_combined_game_stats.csv')
eagles_df = pd.read_csv('NFL\\eagles_combined_game_stats.csv')

# Merge the data based on the 'game' column
df = pd.merge(chiefs_df, eagles_df, on='game', suffixes=('_chiefs', '_eagles'))

# Prepare features for regression - AI told me this was a good way
features = [
    'fumbles_chiefs', 'fumblesLost_chiefs', 'fumblesForced_chiefs', 'fumblesRecovered_chiefs',
    'avgGain_chiefs', 'completionPct_chiefs', 'completions_chiefs',
    'fumbles_eagles', 'fumblesLost_eagles', 'fumblesForced_eagles', 'fumblesRecovered_eagles',
    'avgGain_eagles', 'completionPct_eagles', 'completions_eagles'
]

X = df[features]  # Features from both teams stats
y_chiefs = df['chiefs_score']  # The Chiefs score
y_eagles = df['eagles_score']  # The Eagles score

X_train, X_test, y_train_chiefs, y_test_chiefs, y_train_eagles, y_test_eagles = train_test_split(
    X, y_chiefs, y_eagles, test_size=0.2, random_state=42)

# Create Linear Regression models
model_chiefs = LinearRegression()
model_eagles = LinearRegression()

# Fit the models on the training data
model_chiefs.fit(X_train, y_train_chiefs)
model_eagles.fit(X_train, y_train_eagles)

# Predict on the test set
y_pred_chiefs = model_chiefs.predict(X_test)
y_pred_eagles = model_eagles.predict(X_test)

# Predict scores for a single game
game_index = 0  # AI told me to do this

# Get predicted scores for the Chiefs and Eagles
predicted_score_chiefs = round(y_pred_chiefs[game_index])  # Round
predicted_score_eagles = round(y_pred_eagles[game_index])  # Round

# Print output
print(f"Chiefs: {predicted_score_chiefs}, Eagles: {predicted_score_eagles}")