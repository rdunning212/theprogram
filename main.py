import game_data_service
import game_data_service as gsd
import random
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd

games = game_data_service.get_current_year_dataframe()
games.to_csv('game_data.csv')

game_data = pd.read_csv('game_data.csv')
team_data = pd.read_csv('team_data.csv')

first_team_adj_em = []
first_team_adj_o = []
first_team_adj_d = []
first_team_adj_t = []
first_team_luck = []

second_team_adj_em = []
second_team_adj_o = []
second_team_adj_d = []
second_team_adj_t = []
second_team_luck = []

for index in game_data.index:
    team_name = game_data['Team'][index]
    opponent_name = game_data['Opponent'][index]
    team_one = False
    team_two = False
    for team_index in team_data.index:
        if team_data['Name'][team_index] == team_name:
            first_team_adj_em.append(team_data['AdjEM'][team_index])
            first_team_adj_o.append(team_data['AdjO'][team_index])
            first_team_adj_d.append(team_data['AdjD'][team_index])
            first_team_adj_t.append(team_data['AdjT'][team_index])
            first_team_luck.append(team_data['Luck'][team_index])
            team_one = True
        elif team_data['Name'][team_index] == opponent_name:
            second_team_adj_em.append(team_data['AdjEM'][team_index])
            second_team_adj_o.append(team_data['AdjO'][team_index])
            second_team_adj_d.append(team_data['AdjD'][team_index])
            second_team_adj_t.append(team_data['AdjT'][team_index])
            second_team_luck.append(team_data['Luck'][team_index])
            team_two = True
        if team_one and team_two:
            break

location = list(map(gsd.map_home_away, game_data['Location']))
result = list(map(gsd.map_win_loss, game_data['Result']))

data = {'First AdjEM': first_team_adj_em,
        'First AdjO': first_team_adj_o,
        'First AdjD': first_team_adj_d,
        'First AdjT': first_team_adj_t,
        'First Luck': first_team_luck,
        'Second AdjEM': second_team_adj_em,
        'Second AdjO': second_team_adj_o,
        'Second AdjD': second_team_adj_d,
        'Second AdjT': second_team_adj_t,
        'Second Luck': second_team_luck,
        'Location': location,
        'Result': result
}

for key in data.keys():
    print(len(data[key]))

df = pd.DataFrame(data)
df.to_csv('team_stats_by_game.csv')