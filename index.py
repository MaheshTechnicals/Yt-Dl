import os
from flask import Flask, request, jsonify
from pytube import YouTube

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def get_video_info():
    video_id = request.args.get('videoid')
    quality = request.args.get('quality', 'highest')  # Default to highest quality if not specified

    try:
        yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
        
        # Get the video title
        video_title = yt.title
        
        # Get the appropriate stream based on the requested quality
        if quality == 'highest':
            stream = yt.streams.get_highest_resolution()
        elif quality == 'lowest':
            stream = yt.streams.get_lowest_resolution()
        else:
            stream = yt.streams.get_by_resolution(quality)
        
        # If stream is found, return the URL and title
        if stream:
            video_url = stream.url
            return jsonify({'title': video_title, 'url': video_url})
        else:
            return jsonify({'error': 'Video not found or quality not available'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # Default to port 5000 if not specified
    app.run(debug=True, port=port)
