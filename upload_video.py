import os
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

# File paths
BASE_DIR = "video"
TITLE_FILE = os.path.join(BASE_DIR, "title.txt")
DESCRIPTION_FILE = os.path.join(BASE_DIR, "description.txt")
VIDEO_LINK_FILE = os.path.join(BASE_DIR, "video_link.txt")
THUMBNAIL_LINK_FILE = os.path.join(BASE_DIR, "thumbnail_link.txt")
VIDEO_FILE = "video.mp4"
THUMBNAIL_FILE = "thumbnail.jpg"

def read_file(file_path):
    """Read content from a file."""
    with open(file_path, "r") as f:
        return f.read().strip()

def download_file(url, local_path):
    """Download a file from a URL."""
    print(f"Downloading {url} to {local_path}")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(local_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded {local_path}")

def upload_video_to_youtube(title, description, video_path, thumbnail_path):
    """Upload a video to YouTube."""
    # Load credentials
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)

    # Build the YouTube API client
    youtube = build('youtube', 'v3', credentials=credentials)

    # Video metadata
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['GitHub', 'Automation'],
            'categoryId': '22',  # Category: People & Blogs
        },
        'status': {
            'privacyStatus': 'public',  # Set to 'private' or 'unlisted' if needed
        },
    }

    # Upload video
    print(f"Uploading video: {video_path}")
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    video_request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    )

    response = video_request.execute()
    print(f"Video uploaded: {response['id']}")

    # Upload thumbnail
    print(f"Uploading thumbnail: {thumbnail_path}")
    youtube.thumbnails().set(
        videoId=response['id'],
        media_body=MediaFileUpload(thumbnail_path)
    ).execute()
    print(f"Thumbnail uploaded.")

if __name__ == "__main__":
    # Read metadata from files
    title = read_file(TITLE_FILE)
    description = read_file(DESCRIPTION_FILE)
    video_link = read_file(VIDEO_LINK_FILE)
    thumbnail_link = read_file(THUMBNAIL_LINK_FILE)

    # Download video and thumbnail
    download_file(video_link, VIDEO_FILE)
    download_file(thumbnail_link, THUMBNAIL_FILE)

    # Upload video to YouTube
    upload_video_to_youtube(title, description, VIDEO_FILE, THUMBNAIL_FILE)
