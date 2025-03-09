import yt_dlp
import os

def download_video_as_mp3(url):
    downloads_dir = "downloads"
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)

    def get_video_title(url):
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return info_dict.get('title', 'unknown_title')

    title = get_video_title(url)
    video_dir = os.path.join(downloads_dir, title)

    if not os.path.exists(video_dir):
        os.makedirs(video_dir)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(video_dir, '%(title)s.%(ext)s'),
        'extractaudio': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    download_video_as_mp3(url)