import streamlit as st
from transcriber import transcribe_and_save_video, handle_userinput

def main():
    st.set_page_config(page_title="YouTube Video Transcriber", page_icon=":film_projector:")
    st.header("YouTube Video Transcriber")
    
    # Initialize transcribe_completed and transcript_text in session state if they don't exist
    if 'transcribe_completed' not in st.session_state:
        st.session_state.transcribe_completed = False
    if 'transcript_text' not in st.session_state:
        st.session_state.transcript_text = ""
    
    # Inject custom CSS to style the reset button
    st.markdown("""
    <style>
    .stButton > button:first-child {
        background-color: red;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a reset button
    reset_button = st.button("Reset")
    
    # If the reset button is clicked, reset the session state
    if reset_button:
        st.session_state.transcribe_completed = False
        st.session_state.transcript_text = ""
        st.session_state.current_video_url = ""
    
    st.markdown("<h3 style='color: lightblue; font-weight: bold;'>Paste the YouTube video URL here:</h>", unsafe_allow_html=True)
    video_url_input = st.text_input("", key='video_url_input', value=st.session_state.current_video_url if st.session_state.transcribe_completed else "", disabled=st.session_state.transcribe_completed, label_visibility='hidden')
    video_url = video_url_input if not st.session_state.transcribe_completed else st.session_state.current_video_url
    
    if video_url and not st.session_state.transcribe_completed:
        with st.spinner("Transcribing video..."):
            transcript_text = transcribe_and_save_video(video_url)
            st.write("Video transcribed and saved.")
            st.session_state.transcribe_completed = True
            st.session_state.transcript_text = transcript_text
            st.session_state.current_video_url = video_url
    
    # Display the transcribed text if it exists
    if st.session_state.transcript_text:
        st.write(st.session_state.transcript_text)
    
    # Conditionally display user_question input field based on transcribe_completed
    if st.session_state.transcribe_completed:
        st.markdown("<h3 style='color: lightblue; font-weight: bold;'>Ask a question about the video:</h3>", unsafe_allow_html=True)
        user_question = st.text_input("", key='user_question_input', value="", disabled=False, label_visibility='hidden')
        if user_question:
            response = handle_userinput(user_question)
            st.write(response)

if __name__ == "__main__":
    main()
