import random
import arrow
import cassiopeia as cass
from functionsAndFormulas import *
import time
from sys import *
import json

from cassiopeia.core import Summoner, MatchHistory, Match
from cassiopeia import Queue, Patch

cass.set_riot_api_key( getAPI_key())  # This overrides the value set in your configuration/settings.


def get_match_history(puuid,continent, patch):
    end_time = patch.end
    if end_time is None:
        end_time = arrow.now()
    match_history = MatchHistory(
        continent= continent,
        puuid=puuid,
        queue="ARAM",
        begin_time=patch.start,
        end_time=end_time
    )
    return match_history

def get_match_data(current_match):
    
    regionName = "EUW"
    gameInfo = []
    averageRankList = []
    print("making part pull")
    current_match.participants
    print("part pull success")
    for participant in current_match.blue_team.participants:
        
        cm=cass.get_champion_mastery(participant.summoner, participant.champion, regionName)
        try:
            entry=participant.summoner.league_entries.fives()
            tierNumber=entry.tier._order()[entry.tier]
            divisionNumber=entry.division._order()[entry.division]
            elo = elo_score(tierNumber,divisionNumber)
            averageRankList.append(elo)
        except:
            elo = -1.0
            
        gameInfo.append(participant.champion.id)
        gameInfo.append(cm.points)
        gameInfo.append(participant.summoner.level)
        gameInfo.append(elo)

    for participant in current_match.red_team.participants:
        
        cm=cass.get_champion_mastery(participant.summoner, participant.champion,regionName)
        try:
            entry=participant.summoner.league_entries.fives()
            tierNumber=entry.tier._order()[entry.tier]
            divisionNumber=entry.division._order()[entry.division]
            elo = elo_score(tierNumber,divisionNumber)
            averageRankList.append(elo)
        except:
            elo = -1.0
            
        gameInfo.append(participant.champion.id)
        gameInfo.append(cm.points)
        gameInfo.append(participant.summoner.level)
        gameInfo.append(elo)
    
    gameInfo.append(int(current_match.red_team.win))
    
    print("get match data workds")
    if len(averageRankList)==0:
        return [x if x!=-1.0 else 35.0 for x in gameInfo]
    else:
        averageRank = sum(averageRankList)/len(averageRankList)
        return [x if x!=-1.0 else averageRank for x in gameInfo]

def collect_matches(region, patchStr, unpulled_summoner_ids, 
                    pulled_summoner_ids, unpulled_match_ids, pulled_match_ids):
    
    i=0
    j=0
    
    patch = Patch.from_str(patchStr, region=region)
    
    while unpulled_summoner_ids:
        # Get a random summoner from our list of unpulled summoners and pull their match history
        new_summoner_id = random.choice(unpulled_summoner_ids)
        new_summoner = Summoner(id=new_summoner_id, region=region)
        puuid=new_summoner.puuid
        matches = get_match_history(puuid,summoner.region.continent, patch)
        i=i+1
        print("starting round nr: ", i)
        for match in matches:
            new_match_id=match.id
            if str(match.id)[0]!="E":
                new_match_id="EUW1_"+str(match.id)
            unpulled_match_ids.append(new_match_id)
        unpulled_summoner_ids.remove(new_summoner_id)
        pulled_summoner_ids.append(new_summoner_id)
        while unpulled_match_ids:
            
            # Get a random match from our list of matches
            new_match_id = random.choice(unpulled_match_ids)
            #new_match = Match(id=str(new_match_id), region=region)
            new_match = Match(id=str(new_match_id), region=region)
            
            #get game info and save it in an external txt file
            gameInfo = str(get_match_data(new_match))
            j=j+1
            print("second loop iteration nr: ", j)
            
            with open('match_data_collection.txt','a') as f:
                f.write(gameInfo+'\n')
            
            for participant in new_match.participants:
                if (
                    participant.summoner.id not in pulled_summoner_ids
                    and participant.summoner.id not in unpulled_summoner_ids
                ):
                    unpulled_summoner_ids.append(participant.summoner.id)
            # The above lines will trigger the match to load its data by iterating over all the participants.
            # If you have a database in your datapipeline, the match will automatically be stored in it.
            unpulled_match_ids.remove(new_match_id)
            pulled_match_ids.append(new_match_id)
            
            with open('match_ids.txt','a') as f:
                f.write(new_match_id+'\n')
        print("cleared number of rounds: ", i)
    return pulled_match_ids

if __name__ == "__main__":
    
    
    #"DR4xB0ccfnL7r7Rcuc7jlfvEA8qo08GkIDkX3UHBrXaaStA"
    
    with open('unpulled_summoner_ids', 'r') as f:
        lines = f.read()
    unpulled_summoner_ids = json.loads(lines)
    
    with open('unpulled_match_ids', 'r') as f:
        lines = f.read()
    unpulled_match_ids = json.loads(lines)
    
    with open('pulled_summoner_ids', 'r') as f:
        lines = f.read()
    pulled_summoner_ids = json.loads(lines)
    
    with open('pulled_match_ids', 'r') as f:
        lines = f.read()
    pulled_match_ids = json.loads(lines)
    
    x=collect_matches("EUW", "12.7", unpulled_summoner_ids, pulled_summoner_ids, unpulled_match_ids,
                      pulled_match_ids)
    
    
    
    
    
    
    
    