# import mysql.connector as conn


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
# def grab_video_insights(youtube, videoId)

