import requests
from bs4 import BeautifulSoup
import re

# Replace with your Render service details
service_name = "generated-audio-files"

# Define the base URL for your Render service
base_url = f"https://{service_name}.onrender.com/"

# Function to get the URL of the newest audio file
def get_newest_audio_url():
    # Send a GET request to your Render service
    response = requests.get(base_url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links (anchor tags)
    links = soup.find_all('a')

    # Filter and extract audio file URLs based on naming convention
    audio_urls = [link['href'] for link in links if re.match(r'space_news_summary_\d+\.mp3', link['href'])]

    # Sort the URLs by date (assuming the file names include a date)
    audio_urls.sort()

    # Get the URL of the latest audio file
    if audio_urls:
        latest_audio_url = audio_urls[-1]
        return latest_audio_url

    return None

# Function to download the latest audio file
def download_latest_audio():
    # Get the URL of the newest audio file
    latest_audio_url = get_newest_audio_url()

    if latest_audio_url:
        # Construct the full URL for the latest audio file
        full_audio_url = base_url + latest_audio_url

        # Extract the audio file name from the URL
        file_name = latest_audio_url.split("/")[-1]
        

        # Download the file
        response = requests.get(full_audio_url)
        with open("../generated_audios/generated_audio.mp3", "wb") as f:
            f.write(response.content)
        print(f"Downloaded the latest audio: {file_name}")
    else:
        print("No audio files found.")

# Call the function to download the latest audio
download_latest_audio()