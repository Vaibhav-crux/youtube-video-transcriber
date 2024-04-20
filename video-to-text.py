import streamlit as st
import assemblyai as aai
from pytube import YouTube
import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set your AssemblyAI API key
aai.settings.api_key = "ba1685918c354027ba9118240fd51b64"

# Hardcode the Google API key
GOOGLE_API_KEY = "AIzaSyCvEsb6RYKpdeIMmeOlEP8Gn910H5BocsY"

# Configure the Google Generative AI client with the API key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the transcriber
transcriber = aai.Transcriber()

# Function to transcribe video and save the text to a SQLite database
def transcribe_and_save_video(video_url):
    # Use pytube to download the video
    youtube = YouTube(video_url)
    video = youtube.streams.filter(progressive=True, file_extension='mp4').first()
    video_path = os.path.join(os.getcwd(), video.default_filename)
    video.download(output_path=os.getcwd())
    
    # Check if the video file exists before transcribing
    if not os.path.exists(video_path):
        st.error(f"Video file not found at {video_path}. Please check the URL and try again.")
        return None
    
    # Transcribe the video
    transcript = transcriber.transcribe(video_path)
    
    # Optionally, delete the downloaded video file after transcription
    os.remove(video_path)
    
    # Save the transcript to a SQLite database
    conn = sqlite3.connect('transcriptions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transcriptions (id INTEGER PRIMARY KEY, transcript TEXT)''')
    c.execute("INSERT INTO transcriptions (transcript) VALUES (?)", (transcript.text,))
    conn.commit()
    conn.close()
    
    return transcript.text


# Function to fetch the saved transcript from the database
def fetch_saved_transcript():
    conn = sqlite3.connect('transcriptions.db')
    c = conn.cursor()
    c.execute("SELECT transcript FROM transcriptions ORDER BY id DESC LIMIT 1")
    transcript = c.fetchone()[0]
    conn.close()
    return transcript

# Function to handle user input using Gemini API
def handle_userinput(user_question):
    # Fetch the saved transcript
    transcript = fetch_saved_transcript()
    
    # Use the relevant text along with the user's question to generate a response
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    response = model.generate_content(f"You are a bot. User: {user_question}. Transcript: {transcript}")
    return response.text.strip()

def main():
    st.set_page_config(page_title="YouTube Video Transcriber", page_icon=":film_projector:")
    st.header("YouTube Video Transcriber")
    
    # Initialize transcribe_completed and transcript_text in session state if they don't exist
    if 'transcribe_completed' not in st.session_state:
        st.session_state.transcribe_completed = False
    if 'transcript_text' not in st.session_state:
        st.session_state.transcript_text = ""
    
    # Create a reset button
    reset_button = st.button("Reset")
    
    # If the reset button is clicked, reset the session state
    if reset_button:
        st.session_state.transcribe_completed = False
        st.session_state.transcript_text = ""
        st.session_state.current_video_url = ""
    
    # Disable the video_url input field if transcription is completed
    video_url_input = st.text_input("Paste the YouTube video URL here:", key='video_url_input', value=st.session_state.current_video_url if st.session_state.transcribe_completed else "", disabled=st.session_state.transcribe_completed)
    video_url = video_url_input if not st.session_state.transcribe_completed else st.session_state.current_video_url
    
    if video_url and not st.session_state.transcribe_completed:
        with st.spinner("Transcribing video..."):
            transcript_text = transcribe_and_save_video(video_url)
            st.write("Video transcribed and saved.")
            # Set transcribe_completed to True after transcription is done
            st.session_state.transcribe_completed = True
            # Store the transcribed text in session state
            st.session_state.transcript_text = transcript_text
            # Store the video URL in session state to check if it's the same video being processed
            st.session_state.current_video_url = video_url
    
    # Display the transcribed text if it exists
    if st.session_state.transcript_text:
        st.write(st.session_state.transcript_text)
    
    # Conditionally display user_question input field based on transcribe_completed
    if st.session_state.transcribe_completed:
        user_question = st.text_input("Ask a question about the video:", key='user_question_input', value="", disabled=False)
        if user_question:
            response = handle_userinput(user_question)
            st.write(response)



if __name__ == '__main__':
    main()
