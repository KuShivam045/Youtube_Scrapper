import pandas as pd
from googleapiclient.discovery import build

api_key = "AIzaSyAGkfgU92NZCWR38uxaPfkFhpMn3UtDh7c"
channel_ids = "UC59K-uG2A5ogwIrHw4bmlEg"

channel_ids = ["UC59K-uG2A5ogwIrHw4bmlEg",    #Telusko
    "UCkGS_3D0HEzfflFnG0bD24A",               #MySirG
    "UCXgGY0wkgOzynnHvSEVmE3A",               #Hitesh Choudhary
    "UCNU_lfiiWBdtULKOw6X0Dig"]               #Krish Naik

youtube = build("youtube","v3", developerKey = api_key)
ytube_url  = "https://www.youtube.com/watch?v="

request = youtube.channels().list(part= 'snippet,contentDetails,statistics',id = ','.join(channel_ids))
response = request.execute()
print(response)