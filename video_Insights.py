import mysql.connector as conn

ytube_url  = "https://www.youtube.com/watch?v="

def grab_video_insights(youtube, videoId1):
    
    detail = []

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id= videoId1     
    )
    response = request.execute()

    mydb = conn.connect(host = "localhost", user = "root", passwd = "KuShi025", database = 'Youtube_Scrapper', autocommit=True)
    cursor = mydb.cursor()
    # video_insights = """create table if not exists Videos_Insights(Channel_name varchar(30),Video_title varchar(100), 
    # video_url varchar(50), Publish_Date varchar(20), Views int(15),Video_likes int(10) , Comments_Count int(10), Thumbnail_url varchar(50))"""
    # cursor.execute(video_insights)

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

        sql="""INSERT INTO Videos_Insights ( Video_title, Video_url, Publish_Date, Views, Video_likes, Comments_Count, Thumbnail_url)
        VALUES( %s, %s, %s, %s, %s,%s,%s);"""
        cursor.execute(sql, (Video_title, Video_url, Video_publish_date, Views, Video_Likes, Comments_Count, Thumbnail_url) )


     # print(Video_ID)
        # print(Video_url)
        # print(Video_title)
        # print(Video_publish_date)
        # print(Channel_name)
        # print(Views)
        # print(Video_Likes)
        # print(Comments_Count)
        # print(Thumbnail_url)