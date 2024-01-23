import cassiopeia as cass
from cassiopeia.core import Summoner, MatchHistory, Match
from cassiopeia import Queue, Patch

def getAPI_key():
    f = open("api_key.txt", "r")
    return f.read()

def elo_score(tier, division):
    return tier*10+(division-1)*2.5

def get_match_history(puuid, region, patchStr):
    patch = Patch.from_str(patchStr, region=region)
    summoner_id =
    new_summoner = Summoner(id=summoner_id, region=region)
    continent = summoner.region.continent
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

def get_match_data():

    new_summoner = Summoner(id=new_summoner_id, region=region)
    matches = get_match_history(new_summoner.puuid, new_summoner.region.continent, patch)

def add_mastery_points():
    pass

if __name__ == "__main__":
    searchInfo = {"summoner": "HappyFeet400", "region": "EUW", "patch": "14.1"}
    cass.set_riot_api_key(getAPI_key())



