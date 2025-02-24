import webbrowser
from youtube_search import YoutubeSearch
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Function to get user input (text-based)
def get_input(prompt):
    user_input = input(prompt)  # Get text-based input from the user
    return user_input.lower()  # Convert to lowercase to handle case-insensitive input

# Function to play music
def play_music(song_name):
    """Function to search and play music from Spotify."""
    CLIENT_ID = 'ede91bcab9e04575b479f8426c4e0c2f'  # Replace with your Spotify client ID
    CLIENT_SECRET = '13076ac8fe8040c4954e6593c86293f4'  # Replace with your Spotify client secret
    REDIRECT_URI = 'http://localhost:8888/callback'  # Redirect URI

    # Set up the Spotify API client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope=["user-library-read", "user-read-playback-state", "user-modify-playback-state"]))

    if song_name:
        try:
            # Search for the song on Spotify (without limit)
            results = sp.search(q=song_name, type='track')  # No limit on the number of results
            if results['tracks']['items']:
                # Automatically select the first result
                track = results['tracks']['items'][0]
                music_url = track['external_urls']['spotify']
                print(f"Playing {track['name']} by {track['artists'][0]['name']} on Spotify.")
                webbrowser.open(music_url)  # Open the song in Spotify via the browser
            else:
                print("Sorry, no results found on Spotify.")
        except Exception as e:
            print(f"Error playing music: {e}")

# Function to play video
def play_video(video_name):
    """Function to search and play a video from YouTube."""
    if video_name:
        try:
            # Search for the video on YouTube (without limit)
            results = YoutubeSearch(video_name).to_dict()  # No limit on the number of results
            if results:
                # Automatically select the first result
                video_url = f"https://www.youtube.com{results[0]['url_suffix']}"
                print(f"Playing {results[0]['title']} on YouTube...")
                webbrowser.open(video_url)  # Open the video directly in the browser
            else:
                print("Sorry, no results found on YouTube.")
        except Exception as e:
            print(f"Error playing video: {e}")

# Main function to handle user input and decide whether to play music or video
def main():
    user_input = get_input("What would you like to play?")

    if 'play video' in user_input:
        video_name = user_input.replace('play video', '').strip()
        if video_name:
            play_video(video_name)  # Call function to play video
        else:
            print("Please specify the video name.")
    elif 'play music' in user_input:
        song_name = user_input.replace('play music', '').strip()
        if song_name:
            play_music(song_name)  # Call function to play music
        else:
            print("Please specify the song name.")
    else:
        print("Sorry, I didn't understand your request. Please type 'Play music [song name]' or 'Play video [video name]'.")
