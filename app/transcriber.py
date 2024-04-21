import os
import assemblyai as aai
from pytube import YouTube
import google.generativeai as genai
from dotenv import load_dotenv
from database import save_transcript, fetch_saved_transcript

# Load environment variables
load_dotenv()

# Set your AssemblyAI API key
aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')

# Set your Google API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure the Google Generative AI client with the API key
genai.configure(api_key=GOOGLE_API_KEY)

transcriber = aai.Transcriber()

def transcribe_and_save_video(video_url):
    temp_folder_path = os.path.join(os.path.dirname(os.getcwd()), 'temp')
    
    os.makedirs(temp_folder_path, exist_ok=True)
    
    youtube = YouTube(video_url)
    video = youtube.streams.filter(progressive=True, file_extension='mp4').first()
    video_path = os.path.join(temp_folder_path, video.default_filename)
    video.download(output_path=temp_folder_path)
    
    if not os.path.exists(video_path):
        return None
    
    transcript = transcriber.transcribe(video_path)
    
    # Save the transcript to the database
    save_transcript(transcript.text, video.default_filename)
    
    # Delete the video from the temp folder
    os.remove(video_path)
    
    return transcript.text

def handle_userinput(user_question):
    transcript = fetch_saved_transcript()
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    response = model.generate_content(f"You are a bot. User: {user_question}. Transcript: {transcript}")
    return response.text.strip()
