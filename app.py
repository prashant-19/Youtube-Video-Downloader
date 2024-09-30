import os
import zipfile
import yt_dlp

def download_videos_from_channel(channel_url, download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best', 
        'outtmpl': os.path.join(download_folder, '%(title)s_%(format_id)s.%(ext)s'),  
        'ignoreerrors': True,  
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([channel_url])

def zip_videos(download_folder, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk(download_folder):
            for file in files:
                
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, download_folder))
    print(f"All videos zipped into {zip_filename}")

if __name__ == "__main__":
    channel_url = input("Please enter the YouTube channel's videos URL: ")

    script_path = os.path.dirname(os.path.abspath(__file__))
    download_folder = os.path.join(script_path, "downloaded_videos")
    zip_filename = os.path.join(script_path, "downloaded_videos.zip")

    print("Downloading videos...")
    download_videos_from_channel(channel_url, download_folder)
    print("Videos downloaded successfully.")

    print("Zipping videos...")
    zip_videos(download_folder, zip_filename)

    print("All done! The videos are downloaded and zipped.")
