import mysql.connector as conn
import pandas as pd
from googleapiclient.discovery import build
f = open("test.txt", "a")
f.write("test")
f.close()
api_key = "AIzaSyAGkfgU92NZCWR38uxaPfkFhpMn3UtDh7c"
channel_ids = ["UC59K-uG2A5ogwIrHw4bmlEg",    #Telusko
    "UCkGS_3D0HEzfflFnG0bD24A",               #MySirG
    "UCXgGY0wkgOzynnHvSEVmE3A",               #Hitesh Choudhary
    "UCNU_lfiiWBdtULKOw6X0Dig"]               #Krish Naik

youtube = build("youtube","v3", developerKey = api_key)
ytube_url  = "https://www.youtube.com/watch?v="

request = youtube.channels().list(part= 'snippet,contentDetails,statistics',
                                    id = ','.join(channel_ids))
response = request.execute()

# searchString = request.form['content'].replace(" ","")
# splt = searchString.split("=")
# ytube_url  = splt[0]
# vid_Id = splt[1]

def grab_video_Id(youtube, playlist_id1):
                    
    all_Ids = []
    request = youtube.playlistItems().list(
        part= 'contentDetails',
            
        playlistId = playlist_id1,
        maxResults = 50
    )
    response = request.execute()
    for i in range(len(response["items"])):
        all_Ids.append(response['items'][i]["contentDetails"]["videoId"])
            
    return all_Ids


def grab_video_insights(youtube, videoId1):
            
    detail = []
        
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id= videoId1     
    )
    response = request.execute()
    mydb = conn.connect(host = "localhost", user = "root", passwd = "KuShi025", database = 'Youtube_Scrapper', autocommit=True)
    cursor = mydb.cursor()
    video_insights = """create table if not exists Videos_Insights(Channel_name varchar(30),Video_title varchar(100), 
    video_url varchar(50), Publish_Date varchar(20), Views int(15),Video_likes int(10) , Comments_Count int(10), Thumbnail_url varchar(50))"""
    cursor.execute(video_insights)

    reviews = []
    for i in range(len(response["items"])):
        Video_ID =response['items'][i]["id"]
        Video_url = ytube_url + response['items'][i]["id"]
        Video_title = response['items'][i]['snippet']["title"]
        Video_publish_date = response['items'][i]['snippet']["publishedAt"]
        Channel_name = response['items'][i]['snippet']["channelTitle"]
        Views = response["items"][i]['statistics']["viewCount"]
        Video_Likes = response["items"][i]['statistics']["likeCount"]
        Comments_Count = response["items"][i]['statistics']["commentCount"]
        Thumbnail_url = response['items'][i]['snippet']["thumbnails"]["high"]["url"]


        sql="""INSERT INTO Videos_Insights (Channel_name, Video_title, Video_url, Publish_Date, Views, Video_likes, Comments_Count, Thumbnail_url)
        VALUES(%s, %s, %s, %s, %s, %s,%s,%s);"""
        cursor.execute(sql, (Channel_name, Video_title, Video_url, Video_publish_date, Views, Video_Likes, Comments_Count, Thumbnail_url) )


        mydict = {"Channel_name": Channel_name, "Video_title": Video_title, "Video_url": Video_url, "Views": Views,
                "Video_publish_date": Video_publish_date,"Video_Likes": Video_Likes, "Comments_Count":Comments_Count, "Thumbnail_url": Thumbnail_url}

        reviews.append(mydict)

    return reviews


def get_channel_stats(youtube, channel_ids):
            
    mydb = conn.connect(host = "localhost", user = "root", passwd = "KuShi025", database = 'Youtube_Scrapper', autocommit=True)
    cursor = mydb.cursor()
    for i in range(len(response["items"])):
            
        Channel_name = response["items"][i]['snippet']['title']
        Publish_Date = response["items"][i]['snippet']["publishedAt"]
        subscribers = int(response["items"][i]['statistics']["subscriberCount"])
        video_count = response["items"][i]['statistics']["videoCount"]
        view_count = response["items"][i]['statistics']["viewCount"]
                
        sql="""INSERT INTO Channel_insights (Channel_name, Publish_Date, subscribers, video_count, view_count)
        VALUES(%s, %s, %s, %s, %s);"""
        cursor.execute(sql, (Channel_name, Publish_Date, subscribers, video_count, view_count) )


channel_stats = get_channel_stats(youtube, channel_ids)


def get_channel_stats_df(youtube, channel_ids):
            
    all_data = []
    for i in range(len(response["items"])):
        data = dict(channel_name = str(response["items"][i]['snippet']['title']),
                    Channel_Id= response['items'][i]["id"],
                    Publish_Date = str(response["items"][i]['snippet']["publishedAt"].split("T")),
                    subscribers = response["items"][i]['statistics']["subscriberCount"],
                video_count = response["items"][i]['statistics']["videoCount"],
                view_count = response["items"][i]['statistics']["viewCount"],
                playlist_ID = response["items"][i]["contentDetails"]["relatedPlaylists"]["uploads"])
        all_data.append(data)
                
    df = pd.DataFrame(all_data)
    playId = []
    for i in df["playlist_ID"]:
        playId.append(i)

    playId1 = playId[0]
    playId2 = playId[1]
    playId3 = playId[2]
    playId4 = playId[3]
    lst1 = grab_video_Id(youtube, playId1)
    lst2 = grab_video_Id(youtube, playId2)
    lst3 = grab_video_Id(youtube, playId3)
    lst4 = grab_video_Id(youtube, playId4)
            # print(lst1)


    grab_video_insights(youtube, lst1)
    grab_video_insights(youtube, lst2)
    grab_video_insights(youtube, lst3)
    grab_video_insights(youtube, lst4)
get_channel_stats_df(youtube, channel_ids)
