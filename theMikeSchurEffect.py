from secretsLol import API_KEY, TV, BASE_URL, SEASONS, FILE_NAME_EXT, EPISODE, CREDITS
import requests
import json
import os
from utils import jsonToCSV

def getShowSeasons(showId):
    querySent = {}
    queryRequest = "{0}/{1}/{2}?api_key={3}".format(BASE_URL, TV, showId, API_KEY)
    response = requests.get(queryRequest).json()
        
    seasons = response["seasons"]

    crewList = []
    episodeList = []
    guestList = []
    mainCastList = []

    querySent[str(showId)] = queryRequest

    for season in seasons:
        
        #get show details
        seasonNumber = season["season_number"]
        queryRequest = "{0}/{1}/{2}/{3}/{4}?api_key={5}".format(BASE_URL, TV, showId, SEASONS, seasonNumber, API_KEY)
        response = requests.get(queryRequest).json()
        print(queryRequest)
        episodes = response["episodes"]
        
        querySent[str(showId)+"-"+str(seasonNumber)] = queryRequest
        
        # get specific episode details (cast, crew, guest)
        for episode in episodes:
            episodeNumber = episode["episode_number"]
            episodeId = episode["id"]
            mainCastQuery = "{0}/{1}/{2}/{3}/{4}/{5}/{6}/{7}?api_key={8}".format(BASE_URL, TV, showId, SEASONS, seasonNumber, EPISODE, episodeNumber, CREDITS, API_KEY)
            print(mainCastQuery)
            response = requests.get(mainCastQuery).json()
            mainCrew = response["cast"]
            crew = episode["crew"]
            guestStars = episode["guest_stars"]

            querySent[str(showId)+"-"+str(seasonNumber)+"-"+str(episodeNumber)] = queryRequest

            
            for main in mainCrew:
                main["episodeId"] = episodeId
                main["seasonNumber"] = seasonNumber
                main["episodeNumber"] = episodeNumber
                mainCastList.append(main)
            for c in crew:

                c["episodeId"] = episodeId
                c["seasonNumber"] = seasonNumber
                c["episodeNumber"] = episodeNumber
                crewList.append(c)

            for guest in guestStars:

                guest["episodeId"] = episodeId
                guest["seasonNumber"] = seasonNumber
                guest["episodeNumber"] = episodeNumber
                guestList.append(guest)

            baseObj = {
                "airDate": episode["air_date"],
                "episodeNumber": episodeNumber,
                "id": episode["id"],
                "overview": episode["overview"],
                "voteAverage": episode["vote_average"],
                "voteCount": episode["vote_count"],
            }
            episodeList.append(baseObj)

    jsonToCSV(FILE_NAME_EXT[showId]["seasons"], FILE_NAME_EXT[showId]["showName"], seasons)
    jsonToCSV(FILE_NAME_EXT[showId]["episode"], FILE_NAME_EXT[showId]["showName"], episodeList)
    jsonToCSV(FILE_NAME_EXT[showId]["crew"], FILE_NAME_EXT[showId]["showName"], crewList)
    jsonToCSV(FILE_NAME_EXT[showId]["guest"], FILE_NAME_EXT[showId]["showName"], guestList)
    jsonToCSV(FILE_NAME_EXT[showId]["main"], FILE_NAME_EXT[showId]["showName"], mainCastList)
for showId in FILE_NAME_EXT.keys():
    getShowSeasons(showId)