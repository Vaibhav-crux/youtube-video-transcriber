# YouTube Video Transcriber

This project is a Streamlit web application that transcribes YouTube videos using AssemblyAI and Google Generative AI. It allows users to input a YouTube video URL, transcribes the video, and then uses the transcription to answer questions about the video content. The transcriptions are saved in a SQLite database for future reference.

## Features

- **Video Transcription**: Transcribes YouTube videos using AssemblyAI.
- **Database Storage**: Saves transcriptions in a SQLite database.
- **Question Answering**: Uses Google Generative AI to answer questions based on the transcribed video content.
- **User Interface**: A Streamlit web application with a user-friendly interface.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Streamlit
- AssemblyAI API Key
- Google Generative AI API Key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/youtube-video-transcriber.git
   ```
2. Navigate to the project directory:
   ```
   cd youtube-video-transcriber
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Set up your environment variables:
   - Create a `.env` file in the project root.
   - Add your AssemblyAI API key and Google Generative AI API key:
     ```
     ASSEMBLYAI_API_KEY=your_assemblyai_api_key
     GOOGLE_API_KEY=your_google_api_key
     ```
5. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Usage

1. Open the application in your web browser.
2. Paste the YouTube video URL into the input field.
3. Click the "Transcribe" button to start the transcription process.
4. Once the transcription is complete, you can ask questions about the video content in the provided input field.
5. The application will generate an answer based on the transcription.

## Screenshots

### Main Page
![1](https://github.com/Vaibhav-crux/video-to-textx/assets/122672330/1b084277-dac1-4815-8ff1-bd421111d1b7)

### Processing Transcribe
![2](https://github.com/Vaibhav-crux/video-to-textx/assets/122672330/6a638c97-0e55-4669-8af2-70942663ccb8)

### Transcribe Generated
![3](https://github.com/Vaibhav-crux/video-to-textx/assets/122672330/e9b996ec-7b83-4484-adaf-760a0154fa4a)

### Asked Question
![4](https://github.com/Vaibhav-crux/video-to-textx/assets/122672330/93bf16ce-e6d4-4905-84bd-5c447c78317d)
![5](https://github.com/Vaibhav-crux/video-to-textx/assets/122672330/1fd53784-cf5c-466f-b00f-e9a025e1311e)
