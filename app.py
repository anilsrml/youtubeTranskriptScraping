from flask import Flask, request, render_template
from youtube_transcript_api import YouTubeTranscriptApi
import requests

app = Flask(__name__)

DEEPL_API_KEY = "c6fabddd-51e8-42c2-852a-739dff90ef82:fx"
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_transcript = []
    error = None

    if request.method == 'POST':
        video_url = request.form['video_url']
        try:
            video_id = video_url.split('v=')[-1]
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])

            for entry in transcript:
                response = requests.post(
                    DEEPL_API_URL,
                    headers={"Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"},
                    data={
                        "text": entry["text"],
                        "target_lang": "TR",
                        "source_lang": "EN"
                    }
                )

                if response.status_code == 200:
                    translated_text = response.json()["translations"][0]["text"]
                    translated_transcript.append({
                        "start": entry["start"],
                        "duration": entry["duration"],
                        "text": translated_text
                    })
                else:
                    error = f"Translation API Error: {response.text}"
                    break
        except Exception as e:
            error = str(e)

    return render_template('index.html', translations=translated_transcript, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)