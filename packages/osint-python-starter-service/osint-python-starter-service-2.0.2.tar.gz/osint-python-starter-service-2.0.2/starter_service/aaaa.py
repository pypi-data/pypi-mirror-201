from youtube_transcript_api import YouTubeTranscriptApi

video_id = "Byh1LiGOd88"
transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ru'])
print(transcript)
