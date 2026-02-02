import os
from dotenv import load_dotenv

load_dotenv()

class SpotifyMoodPlaylist:
    def __init__(self, mock_mode=True):
        self.mock_mode = mock_mode or not os.getenv('SPOTIFY_CLIENT_ID')
        
        if not self.mock_mode:
            import spotipy
            from spotipy.oauth2 import SpotifyOAuth
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
                scope='playlist-modify-public playlist-modify-private'
            ))
        else:
            print("⚠️  Running in MOCK mode (Spotify API unavailable)")
    
    def get_mood_tracks(self, emotion, count=20):
        """Get tracks based on emotion"""
        if self.mock_mode:
            # Return mock track URIs
            mock_tracks = {
                'positive': ['spotify:track:mock_happy_' + str(i) for i in range(count)],
                'negative': ['spotify:track:mock_sad_' + str(i) for i in range(count)],
                'neutral': ['spotify:track:mock_neutral_' + str(i) for i in range(count)]
            }
            return mock_tracks.get(emotion, mock_tracks['neutral'])
        
        # Real Spotify logic here (when API is available)
        mood_params = {
            'positive': {'valence': (0.6, 1.0), 'energy': (0.5, 1.0)},
            'negative': {'valence': (0.0, 0.4), 'energy': (0.3, 0.7)},
            'neutral': {'valence': (0.4, 0.6), 'energy': (0.4, 0.6)}
        }
        
        params = mood_params.get(emotion, mood_params['neutral'])
        genres = ['pop', 'rock', 'electronic', 'indie']
        tracks = []
        
        for genre in genres[:2]:
            results = self.sp.search(q=f'genre:{genre}', type='track', limit=count//2)
            tracks.extend([t['uri'] for t in results['tracks']['items']])
        
        return tracks[:count]
    
    def create_mood_playlist(self, name, description, tracks):
        """Create playlist with tracks"""
        if self.mock_mode:
            mock_url = f"https://open.spotify.com/playlist/mock_{name.replace(' ', '_')}"
            print(f"\n🎵 [MOCK] Playlist '{name}' would be created with {len(tracks)} tracks")
            print(f"📝 Description: {description}")
            return mock_url
        
        # Real Spotify logic
        user_id = self.sp.current_user()['id']
        playlist = self.sp.user_playlist_create(
            user=user_id, name=name, public=False, description=description
        )
        
        if tracks:
            self.sp.playlist_add_items(playlist['id'], tracks)
        
        return playlist['external_urls']['spotify']

# Test function
if __name__ == "__main__":
    sp_manager = SpotifyMoodPlaylist(mock_mode=True)
    tracks = sp_manager.get_mood_tracks('positive', 10)
    url = sp_manager.create_mood_playlist('Test Playlist', 'Testing', tracks)
    print(f"Playlist URL: {url}")
