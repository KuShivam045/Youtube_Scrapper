from googleapiclient.discovery import build
from Video_id import grab_video_Id
from video_Insights import grab_video_insights
import mysql.connector as conn


api_key = "AIzaSyAGkfgU92NZCWR38uxaPfkFhpMn3UtDh7c"
channel_ids = ["UC59K-uG2A5ogwIrHw4bmlEg",    #Telusko
    "UCkGS_3D0HEzfflFnG0bD24A",               #MySirG
    "UCXgGY0wkgOzynnHvSEVmE3A",               #Hitesh Choudhary
    "UCNU_lfiiWBdtULKOw6X0Dig"]               #Krish Naik

youtube = build("youtube","v3", developerKey = api_key)

ytube_url  = "https://www.youtube.com/watch?v="

def get_channel_stats(youtube, channel_ids):

    request = youtube.channels().list(part= 'snippet,contentDetails,statistics',id = ','.join(channel_ids))
    response = request.execute()

    
    all_data = []

    mydb = conn.connect(host = "localhost", user = "root", passwd = "KuShi025", database = 'Youtube_Scrapper', autocommit=True)
    cursor = mydb.cursor()
    #video_insights = """create table if not exists Channel_Insights(Channel_name varchar(30), Publish_Date varchar(30),
    #subscribers int(10), video_count int(10), view_count int(15))"""
    #cursor.execute(video_insights)
    #cursor.execute("ALTER TABLE `Channel_Insights` ADD `Id` INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE;")
    # cursor.execute("ALTER TABLE Channel_Insights AUTO_INCREMENT = 1;")

    for i in range(len(response["items"])):
    
        Channel_name = response["items"][i]['snippet']['title']
        Publish_Date = response["items"][i]['snippet']["publishedAt"]
        subscribers = int(response["items"][i]['statistics']["subscriberCount"])
        video_count = response["items"][i]['statistics']["videoCount"]
        view_count = response["items"][i]['statistics']["viewCount"]
        playlist_ID = response["items"][i]["contentDetails"]["relatedPlaylists"]["uploads"]

        all_data.append(playlist_ID)

        sql="""INSERT INTO Channel_insights (Channel_name, Publish_Date, subscribers, video_count, view_count)
        VALUES(%s, %s, %s, %s, %s);"""
        cursor.execute(sql, (Channel_name, Publish_Date, subscribers, video_count, view_count) )

    # playId1 = all_data[0]
    # playId2 = all_data[1]
    # playId3 = all_data[2]
    # playId4 = all_data[3]    

    lst1 = grab_video_Id(youtube, all_data[0])
    grab_video_insights(youtube,lst1)

    lst2 = grab_video_Id(youtube, all_data[1])
    grab_video_insights(youtube,lst2)

    lst3 = grab_video_Id(youtube, all_data[2])
    grab_video_insights(youtube,lst3)

    lst4 = grab_video_Id(youtube, all_data[3])
    grab_video_insights(youtube,lst4)
    # print(ls3)
channel_stats = get_channel_stats(youtube, channel_ids)