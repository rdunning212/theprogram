import random
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd

def tryInt(myInt):  #checks if a string is an int (becomes relevant once brackets are announced)
    try:
        int(myInt)
        return True
    except:
        return False


def get_games_by_team_current_year(team_name):   #scrapes the data from the website
    url_team_name = team_name.replace(" ", "+")
    url_team_name = url_team_name.replace("&", "%26")
    page_url = "https://kenpom.com/team.php?team="+url_team_name
    page_headers = {'User-Agent': 'Mozilla/5.0', 'cookie': '_ga=GA1.2.1656013931.1650149832; _gid=GA1.2.1345748452.1650149832; __stripe_mid=18e728cc-1447-4e23-84cb-39fc19cb09dce84499; __stripe_sid=e8b0227c-39d4-428b-8058-8242aac6b7fcebfabb; PHPSESSID=c1129f32780cce059aabcb71fbcb5a05; kenpomuser=rdunning4242%40gmail.com; kenpomid=345df40ab647fa5e3da0576f67b37821'}
    req = Request(page_url, headers=page_headers)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find("table", {"id": "schedule-table"})
    data_body = table.tbody
    all_games = []
    game_list = []
    for tag in data_body("tr"):
        game_list.append(tag("td"))
    for game in game_list:
        game_info = []
        for item in game:
            if item.a:
                if item.a.string:
                    game_info.append(item.a.string)
                if item.a.b:
                    game_info.append(item.a.b.string)
        if len(game_info) == 4:
            game_info.insert(0, team_name)
            all_games.append(game_info)
    return all_games


def get_team_names():   #scrapes the data from the website
    page_url = "https://kenpom.com/"
    page_headers = {'User-Agent': 'Mozilla/5.0'}
    req = Request(page_url, headers=page_headers)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find("table")
    data_body = table.tbody
    team_list_crappy = []
    team_list_less_crappy = []
    team_list = []
    for tag in data_body("tr"):
        team_list_crappy.append(tag("td"))
    for team in team_list_crappy:
        if not team == []:
            team_list_less_crappy.append(team)
    for i in team_list_less_crappy:
        t = []
        t.append(i[1].a.string)
        if not (tryInt(t[0])):
            team_list.append(t[0])
    return team_list


def get_games_all_teams_current_year():
    all_games = []
    all_teams = get_team_names()
    for team in all_teams:
        try:
            team_games = get_games_by_team_current_year(team)
            all_games = all_games + team_games
        except Exception as e:
            print("Error getting data for team:", team, "Error:", e)

    return all_games

def get_all_team_stats():   #scrapes the data from the website
    page_url = "https://kenpom.com/"
    page_headers={'User-Agent': 'Mozilla/5.0'}
    req = Request(page_url, headers=page_headers)

    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

    table = soup.find("table")
    data_body = table.tbody

    team_list_crappy = []
    team_list_less_crappy = []
    team_list = []

    for tag in data_body("tr"):
        team_list_crappy.append(tag("td"))
    for team in team_list_crappy:
        if not team == []:
            team_list_less_crappy.append(team)
    for i in team_list_less_crappy:
        t = []
        t.append(i[1].a.string)
        t.append(float(i[4].string))
        t.append(float(i[5].string))
        t.append(float(i[7].string))
        t.append(float(i[9].string))
        t.append(float(i[11].string))
        if not (tryInt(t[0])):
            team_list.append(t)

    names = [team[0] for team in team_list]
    adj_em = [team[1] for team in team_list]
    adj_o = [team[2] for team in team_list]
    adj_d = [team[3] for team in team_list]
    adj_t = [team[4] for team in team_list]
    luck = [team[5] for team in team_list]

    data = {'Name': names, 'AdjEM': adj_em, 'AdjO': adj_o, 'AdjD': adj_d, 'AdjT': adj_t, 'Luck': luck}
    df = pd.DataFrame(data)

    return df


def get_current_year_dataframe():
    all_games = get_games_all_teams_current_year()
    team = []
    date = []
    opponent = []
    result = []
    location = []
    for game in all_games:
        team.append(game[0])
        date.append(game[1])
        opponent.append(game[2])
        result.append(game[3])
        location.append(game[4])
    data = {'Team': team, 'Date': date, 'Opponent': opponent, 'Result': result, 'Location': location}
    df = pd.DataFrame(data)

    return df


def map_home_away(loc):
    if 'Home' in loc:
        return 1
    elif 'Away' in loc:
        return -1
    else:
        return 0


def map_win_loss(result):
    if result == 'W':
        return 1
    else:
        return 0
