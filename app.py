from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
import yt_dlp
import os
import webbrowser
import threading

app = Flask(__name__)

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
        'noplaylist': True,
    }

    output = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        output.append(f"Successfully downloaded {title}.")
    except Exception as e:
        output.append(f"Error: {e}")

    return title, os.path.join(video_dir, f"{title}.mp3"), "\n".join(output)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    if url:
        title, video_path, result = download_video_as_mp3(url)
        return jsonify({'title': title, 'output': result, 'download_link': url_for('download_file', filename=f"{title}/{title}.mp3")})
    return jsonify({'output': 'No URL provided.'}), 400

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory('downloads', filename, as_attachment=True)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)