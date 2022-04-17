import time
import random
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

"""
requires beautifulsoup library

install by typing "py -m pip install beautifulsoup4" in command line (for windows)

"""




def sim_matchup(first_current_team, second_current_team, all_teams):
    print("simming, please wait")

    averages= leagueAverages(all_teams) #calls function to get league averages
    
    first_current_team_seasonpace = first_current_team[3]   #calculates projected game pace
    second_current_team_seasonpace = second_current_team[3]
    ncaa_average_pace = averages[0]
    game_pace = ((first_current_team_seasonpace) * (second_current_team_seasonpace)) // (ncaa_average_pace)


    ncaa_average_efficiency = averages[1]/100   #calculates each team's projected efficiencies
    first_current_team_seasonoffeff = first_current_team[1]/100
    second_current_team_seasonoffeff = second_current_team[1]/100
    first_current_team_seasondefeff = first_current_team[2]/100
    second_current_team_seasondefeff = second_current_team[2]/100


    first_current_team_projeff = ((first_current_team_seasonoffeff) * (second_current_team_seasondefeff)) / ncaa_average_efficiency
    
    second_current_team_projeff = ((second_current_team_seasonoffeff) * (first_current_team_seasondefeff)) / ncaa_average_efficiency
    

    first_current_team_score = (game_pace) * (first_current_team_projeff)   #each team's projected score
    
    second_current_team_score = (game_pace) * (second_current_team_projeff)
    

    #calculate standard deviation from score
    first_current_team_standard_deviation = (4 * (game_pace) * ((first_current_team_projeff) / 2) * (1 - ((first_current_team_projeff) / 2))) ** .5
    second_current_team_standard_deviation = (4 * (game_pace) * ((second_current_team_projeff) / 2) * (1 - ((second_current_team_projeff) / 2))) ** .5

    first_current_team_sims_won = 0
    second_current_team_sims_won = 0

    #simulate matchup and count each team's victories
    for t in range(100001):

        first_current_team_final_score = random.gauss((first_current_team_score), (first_current_team_standard_deviation))
        second_current_team_final_score = random.gauss((second_current_team_score), (second_current_team_standard_deviation))

        
        if first_current_team_final_score > second_current_team_final_score:
            first_current_team_sims_won = (first_current_team_sims_won) + 1
        elif first_current_team_final_score < second_current_team_final_score:
            second_current_team_sims_won = (second_current_team_sims_won) + 1
        elif first_current_team_final_score == second_current_team_final_score:
            t = t - 1
    if first_current_team_sims_won > second_current_team_sims_won:
        winning_team = first_current_team[0]
        chance_of_victory = (first_current_team_sims_won) // 1000
        sim_winner = first_current_team
    elif first_current_team_sims_won < second_current_team_sims_won:
        winning_team = second_current_team[0]
        chance_of_victory = (second_current_team_sims_won) // 1000
        sim_winner = second_current_team


    return sim_winner, chance_of_victory, first_current_team_score, second_current_team_score

def tryInt(myInt):  #checks if a string is an int (becomes relevant once brackets are announced)
    try:
        int(myInt)
        return True
    except:
        return False


def leagueAverages(all_teams):  #gets league averages
    efficiencyAverage=0
    tempoAverage=0
    for x in range(len(all_teams)):

        tempoAverage+= all_teams[x][3]

        efficiencyAverage+= all_teams[x][1] +all_teams[x][2]

    efficiencyAverage= (round((efficiencyAverage/(len(all_teams)*2)),3))
    tempoAverage= (round((tempoAverage/len(all_teams)),1))
    return efficiencyAverage, tempoAverage


def scrapeData():   #scrapes the data from the website
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
    team_list2 = []
    for tag in data_body("tr"):
        team_list_crappy.append(tag("td"))
    for team in team_list_crappy:
        if not team == []:
            team_list_less_crappy.append(team)
    for i in team_list_less_crappy:
        t = []
        t.append(i[1].a.string)
        t.append(float(i[5].string))
        t.append(float(i[7].string))
        t.append(float(i[9].string))
        if not (tryInt(t[0])):
            team_list.append(t)
    return team_list

teams = scrapeData()



done = False
while not done:
    print("Would you like to simulate a matchup?") #asks to simulate a matchup
    print("1. Yes")
    print("2. No")
    y = int(input())
    if y == 1:
        found_teams=[]
        print("Search for First Team:") #searches for first team
        search_term = input()
        for w in range(len(teams)):
            if search_term.lower() in teams[w][0].lower():
                found_teams.append(teams[w])
        
        if len(found_teams) > 0:
            print("")
            print("Choose From These Teams: ")  #select first team
            for x in range(len(found_teams)):
                print(str(x+1)+".", found_teams[x][0])
                
            choice= int(input("Number of Choice: "))
            print("")
            first_current_team= found_teams[choice-1]
            
        print("")
        print("")
        found_teams=[]
        print("Search for Second Team:")    
        search_term = input()
        for w in range(len(teams)):
            if search_term.lower() in teams[w][0].lower():
                found_teams.append(teams[w])
        
        if len(found_teams) > 0:
            print("")
            print("Choose From These Teams: ")
            for x in range(len(found_teams)):
                print(str(x+1)+".", found_teams[x][0])
    
            choice= int(input("Number of Choice: "))
            print("")
            second_current_team= found_teams[choice-1]
            
        result = sim_matchup(first_current_team, second_current_team, teams) #simulate matchup
        sim_winner = result[0]
        chance_of_victory = result[1]
        first_current_team_score = result[2]
        second_current_team_score = result[3]
        print("")
        print(first_current_team[0], " vs. ", second_current_team[0])
        print("Winner: ", sim_winner[0])
        print("Chance of Victory: ", chance_of_victory, "%")
        print("Score: ", first_current_team[0], ": ", first_current_team_score, ", ", second_current_team[0], ": ",
              second_current_team_score)
        print("")
    elif y == 2:
        done = True













