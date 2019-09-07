api_key="AIzaSyBoETqNFSqKjTSyi6tlLpx3kjY_S8a05v4"
from apiclient.discovery import build
youtube=build('youtube','v3',developerKey=api_key)

list_videos=set()
for keyword in ['mt4','mt5','metatrader','algo trading','forex','expert advisor','ea mql5','ea mql4']:
    for order in ["viewCount","relevance","rating","date"]:
        request = youtube.search().list(relevanceLanguage="en",part="snippet",maxResults=50,q=keyword,type="video", order=order)
        response = request.execute()

        for item in response['items']:
            list_videos.add(item['id']['videoId'])

file = open('video_id.txt', 'w')
for i in list_videos:
    file.write(i+"\n")
file.close()



file = open('video_id.txt', 'r')
for i in file:
    print(i)
file.close()

