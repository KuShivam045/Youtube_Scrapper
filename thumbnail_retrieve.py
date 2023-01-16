import os
import requests


def persist_image(folder_path,thumbnail_url):
    
#     path = r"C:\Users\Shivaay\thumbnails"
    url = thumbnail_url
    try:
        if not os.path.exists(folder_path):
#             os.makedirs(folder_path)
            os.chdir(os.path.join(os.getcwd(), folder_path))
            os.mkdir(os.path.join(os.getcwd(), folder_path))
    except:
        pass
#     os.chdir(os.path.join(os.getcwd(), folder_path))
    
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")
  

    try:
        f = open(os.path.join(folder_path + ".jpg" ), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as Image + '/' ")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

persist_image('thumbnails',thumbnail_url)