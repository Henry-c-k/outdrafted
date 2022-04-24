import cassiopeia as cass
from cassiopeia import Summoner, FeaturedMatches, Champion, ChampionMastery, Queue, Position, Rank

def getAPI_key():
    f = open("api_key.txt", "r")
    return f.read()

cass.set_riot_api_key(getAPI_key())  # This overrides the value set in your configuration/settings.

def elo_score(Tier: int, Division: int):
    return Tier*10+(Division-1)*2.5

def Average(lst):
    return sum(lst) / len(lst)

def get_match_data(name: str, region: str):

    summoner = Summoner(name=name, region=region)
    gameregion=summoner.region
    current_match = summoner.current_match
    print(current_match.map.name)
    print(current_match.id)
    print()
    elo_average = []

    print("\033[1;34;47m Blue Team \033[0m" )
    for participant in current_match.blue_team.participants:
        print(participant.summoner.name)
        print("Summoner Level:", participant.summoner.level)
        
        try:
            entry=participant.summoner.league_entries.fives
            print(entry.tier, entry.division)
            TierNumber=entry.tier._order()[entry.tier]
            divisionNumber=entry.division._order()[entry.division]
            # print("Division Number:" , divisionNumber)
            # print("Tier Number:" , TierNumber)
            elo = elo_score(TierNumber,divisionNumber)
            print("Elo Score" , elo)
            elo_average.append(elo)
        except: 
            print("Player not ranked or buggy")
            print("Silver 2")
            print("Elo Score", 35)
        
        print(participant.champion.name, participant.champion.id)
        cm = cass.get_champion_mastery(champion=participant.champion, summoner=participant.summoner, region=gameregion)
        print("Mastery points:", cm.points)
        print()
        
    print()
    print("\033[1;31;47m Red Team \033[0m")
    for participant in current_match.red_team.participants:
        print(participant.summoner.name)
        print("Summoner Level:", participant.summoner.level)
        
        try:
            entry=participant.summoner.league_entries.fives
            print(entry.tier, entry.division)
            TierNumber=entry.tier._order()[entry.tier]
            divisionNumber=entry.division._order()[entry.division]
            # print("Division Number:" , divisionNumber)
            # print("Tier Number:" , TierNumber)
            elo = elo_score(TierNumber,divisionNumber)
            print("Elo Score" , elo)
            elo_average.append(elo)
            
        except: 
            print("Player not ranked or buggy")
            print("Silver 2")
            print("Elo Score", 35)

        print(participant.champion.name, participant.champion.id)
        cm = cass.get_champion_mastery(champion=participant.champion, summoner=participant.summoner, region=gameregion)
        print("Mastery points:", cm.points)
        print()
        
    if len(elo_average)==0:
        print("All players unranked")
    else:
        print("Elo Average:" , Average(elo_average))
        
        


if __name__ == "__main__":
    get_match_data("Seraphineas", "EUW")
    #test
