import os
import zipfile
import yt_dlp

def download_videos_from_channel(channel_url, download_folder, archive_file):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': os.path.join(download_folder, '%(title)s_%(format_id)s.%(ext)s'),
        'ignoreerrors': True,
        'download_archive': archive_file,  # Tracks completed downloads
        'continuedl': True,               # Continue partially downloaded files
        'noplaylist': False,              # Ensure playlist videos are downloaded
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

def get_channel_name(channel_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        return info.get('title', 'unknown_channel').replace(' ', '_')

if __name__ == "__main__":
    channel_urls = [
        "https://www.youtube.com/@channel_name/videos"
    ]

    script_path = os.path.dirname(os.path.abspath(__file__))

    for channel_url in channel_urls:
        print(f"Processing {channel_url}...")
        channel_name = get_channel_name(channel_url)

        download_folder = os.path.join(script_path, channel_name)
        archive_file = os.path.join(download_folder, "downloaded_videos.txt")  # Tracks downloaded videos
        zip_filename = os.path.join(script_path, f"{channel_name}.zip")

        print(f"Downloading videos for {channel_name}...\nThis will resume any incomplete downloads.")
        download_videos_from_channel(channel_url, download_folder, archive_file)
        print(f"Videos downloaded successfully for {channel_name}.")

        print(f"Zipping videos for {channel_name}...")
        zip_videos(download_folder, zip_filename)

    print("All done! The videos from all channels are downloaded and zipped.")
