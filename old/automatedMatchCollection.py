import random
import arrow
import cassiopeia as cass
import json
import numpy as np
import time
from sys import *
from functionsAndFormulas import *
from cassiopeia.core import Summoner, MatchHistory, Match
from cassiopeia import Queue, Patch

cass.set_riot_api_key(getAPI_key())

def get_match_history(puuid, continent, patch):
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
    print(current_match.id)
    
    current_match.participants
    for participant in current_match.blue_team.participants:
        
        print(current_match.patch)
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
    gameInfo.append(current_match.id)
    
    if len(averageRankList)==0:
        return [x if x!=-1.0 else 35.0 for x in gameInfo]
    else:
        averageRank = round(sum(averageRankList)/len(averageRankList),2)
        return [x if x!=-1.0 else averageRank for x in gameInfo]

def collect_matches(unpulled_summoner_ids, pulled_summoner_ids, unpulled_match_ids, pulled_match_ids, region : str, patchStr : str):
    
    i=0
    patch = Patch.from_str(patchStr, region=region)
    while unpulled_summoner_ids:
        new_summoner_id = random.choice(unpulled_summoner_ids)
        new_summoner = Summoner(id=new_summoner_id, region=region)
        matches = get_match_history(new_summoner.puuid, new_summoner.region.continent, patch)
        
        for match in matches:
            new_match_id=match.id
            if str(match.id)[0]!="E":
                new_match_id="EUW1_"+str(match.id)
            unpulled_match_ids.append(new_match_id)
            
        np.savetxt('unpulled_match_ids.txt',unpulled_match_ids, fmt='%s')
        unpulled_summoner_ids.remove(new_summoner_id)
        np.savetxt('unpulled_summoner_ids.txt', unpulled_summoner_ids, fmt = '%s')
        pulled_summoner_ids.append(new_summoner_id)
        np.savetxt('pulled_summoner_ids.txt', pulled_summoner_ids, fmt = '%s')
        
        while unpulled_match_ids:
            
            # Get a random match from our list of matches
            new_match_id = random.choice(unpulled_match_ids)
            
            #new_match = Match(id=str(new_match_id), region=region)
            print("new match id: ", new_match_id)
            new_match = Match(id=str(new_match_id), region=region)
            
            #get game info and save it in an external txt file
            try:
                gameInfo = get_match_data(new_match)
                with open('match_data_collection.txt','a') as f:
                    f.write(str(gameInfo)+'\n')
            except:
                print("game bugged go to next")
            
            for participant in new_match.participants:
                if (
                    participant.summoner.id not in pulled_summoner_ids
                    and participant.summoner.id not in unpulled_summoner_ids
                ):
                    unpulled_summoner_ids.append(participant.summoner.id)
            np.savetxt('unpulled_summoner_ids.txt', unpulled_summoner_ids, fmt = '%s')
            # The above lines will trigger the match to load its data by iterating over all the participants.
            # If you have a database in your datapipeline, the match will automatically be stored in it.
            unpulled_match_ids.remove(new_match_id)
            np.savetxt('unpulled_match_ids.txt', unpulled_match_ids, fmt = '%s')
            pulled_match_ids.append(new_match_id)
            np.savetxt('pulled_match_ids.txt', pulled_match_ids, fmt = '%s')
            
            
            i=i+1
            print("Matches pulled: ", i)
            
    return pulled_match_ids

def get_unpulled_summoner_id(pulled_summoner_ids, unpulled_match_ids, region):
    
    for match_id in unpulled_match_ids:
        new_match = Match(id=str(match_id), region=region)
        print("its a match")
        for participant in new_match.participants:
            if participant.summoner.id not in pulled_summoner_ids:
                return participant.summoner.id

if __name__ == "__main__":
    
    #import previously gathered data back into lists
    try:
        unpulled_summoner_ids=np.loadtxt('unpulled_summoner_ids.txt', dtype='str').tolist().split()
    except:
        try:
            unpulled_summoner_ids=np.loadtxt('unpulled_summoner_ids.txt', dtype='str').tolist()
        except:
            unpulled_summoner_ids=[]
    try:
        pulled_summoner_ids=np.loadtxt('pulled_summoner_ids.txt', dtype='str').tolist().split()
    except:
        try:
            pulled_summoner_ids=np.loadtxt('pulled_summoner_ids.txt', dtype='str').tolist()
        except:
            pulled_summoner_ids=[]
    try:
        unpulled_match_ids=np.loadtxt('unpulled_match_ids.txt', dtype='str').tolist().split()
    except:
        try:
            unpulled_match_ids=np.loadtxt('unpulled_match_ids.txt', dtype='str').tolist()
        except:
            unpulled_match_ids=[]
    try:
        pulled_match_ids=np.loadtxt('pulled_match_ids.txt', dtype='str').tolist().split()
    except:
        try:
            pulled_match_ids=np.loadtxt('pulled_match_ids.txt', dtype='str').tolist()
        except:
            pulled_match_ids=[]
        
    #make sure that unpulled_summoners_ids isnt empty so that the collect_matches can function
    if len(unpulled_summoner_ids)==0:
        print("no unpulled ids")
        starting_id = get_unpulled_summoner_id(pulled_summoner_ids, unpulled_match_ids, "EUW")
        unpulled_summoner_ids.append(starting_id)
    print(unpulled_summoner_ids)
    
    collect_matches(unpulled_summoner_ids, pulled_summoner_ids, unpulled_match_ids, pulled_match_ids, "EUW", "12.7")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    