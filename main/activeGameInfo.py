import cassiopeia as cass
from cassiopeia import Summoner
from functionsAndFormulas import *

"""
additional data to consider:
    runes, summoner spells, premades, hot streaks/ losing streak,
    season champion played, 
    number tanks(engange)/ adcs / mages etc.
    time to win / kill advantage (game is stomp yes or no)
"""

cass.set_riot_api_key( getAPI_key())  # This overrides the value set in configuration/settings.

def get_match_data(name : str, region : str):
    summoner = Summoner(name=name, region=region)
    regionName=summoner.region
    current_match = summoner.current_match
    
    gameInfo = []
    averageRankList = []
   
    #a_summoner_name = match.blue_team.participants[0].summoner.name
    #print(match.queue)     
    print("match id: ",current_match.id)
    print("map name: ", current_match.map.name)
    print("---------------------")
     
    print("blue team ")
    for participant in current_match.blue_team.participants:
        print("champion name: ", participant.summoner.name)
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("puuid: ", participant.summoner.puuid)
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("champion id: ", participant.champion.id)         
        cm=cass.get_champion_mastery(participant.summoner, participant.champion, regionName)
        print("mastery points: ",cm.points)
        print("summoner level: ", participant.summoner.level) 
          
        try:
            entry=participant.summoner.league_entries.fives()
            tierNumber=entry.tier._order()[entry.tier]
            divisionNumber=entry.division._order()[entry.division]
            print("tier : ",entry.tier)
            print("division : ",entry.division) 
            elo = elo_score(tierNumber,divisionNumber)
            print("elo: ", elo)
            averageRankList.append(elo)
        except:
            elo = -1.0
            print("not ranked -> use rank silver 2; elo: ", elo)
            
        gameInfo.append(participant.champion.id)
        gameInfo.append(cm.points)
        gameInfo.append(participant.summoner.level)
        gameInfo.append(elo)

    print("red team ")
    for participant in current_match.red_team.participants:
        print("champion name: ", participant.summoner.name)
        print("champion id: ", participant.champion.id)
        cm=cass.get_champion_mastery(participant.summoner, participant.champion,regionName)
        print("mastery points: ",cm.points)
        print("summoner level: ", participant.summoner.level) 
        
        try:
            entry=participant.summoner.league_entries.fives()
            tierNumber=entry.tier._order()[entry.tier]
            divisionNumber=entry.division._order()[entry.division]
            print("tier : ",entry.tier)
            print("division : ",entry.division) 
            elo = elo_score(tierNumber,divisionNumber)
            print("elo: ",elo)
            averageRankList.append(elo)
        except:
            elo = -1.0
            print("not ranked -> use rank silver 2; elo: ", elo)
            
        gameInfo.append(participant.champion.id)
        gameInfo.append(cm.points)
        gameInfo.append(participant.summoner.level)
        gameInfo.append(elo)
    print()
    
    if len(averageRankList)==0:
        return [x if x!=-1.0 else 35.0 for x in gameInfo]
    else:
        averageRank = sum(averageRankList)/len(averageRankList)
        print("average rank: ", averageRank)
        return [x if x!=-1.0 else averageRank for x in gameInfo]
   

   
         

if __name__ == "__main__":
    gameInfo = get_match_data("zafccp", "EUW")
    print(gameInfo)