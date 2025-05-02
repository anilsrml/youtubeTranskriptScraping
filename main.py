from youtube_transcript_api import YouTubeTranscriptApi

# Video ID'sini buraya girin
video_id = ""

try:
    # Türkçe otomatik oluşturulmuş transkripti almak için 'tr' dili belirtiliyor
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])

    # Her bir transkript bloğunu ekrana yazdırıyoruz
    for entry in transcript:
        start = entry.get("start", 0)
        duration = entry.get("duration", 0)
        text = entry.get("text", "")
        print(f"Başlangıç: {start:.2f}s, Süre: {duration:.2f}s, Metin: {text}")
except Exception as e:
    print("Transkript alınırken hata oluştu:", e)
