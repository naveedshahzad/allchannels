import os
import subprocess
from datetime import datetime, timedelta
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle
import json
from google.oauth2.credentials import Credentials

# File paths
BASE_DIR = "video"
TITLE_FILE = os.path.join(BASE_DIR, "title.txt")
DESCRIPTION_FILE = os.path.join(BASE_DIR, "description.txt")
VIDEO_LINK_FILE = os.path.join(BASE_DIR, "video_link.txt")
THUMBNAIL_LINK_FILE = os.path.join(BASE_DIR, "thumbnail_link.txt")
VIDEO_FILE = "video.mp4"
THUMBNAIL_FILE = "thumbnail.jpg"
GITHUB_TOKEN_FILE = "gh_token.txt"
CHANNEL_ID_FILE = "channel_id.txt"

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

import requests

# Replace with your GitHub details
REPO_OWNER = "naveedshahzad"
REPO_NAME = "allchannels"
GITHUB_TOKEN = read_file(GITHUB_TOKEN_FILE)  # Your GitHub personal access token
BRANCH_NAME = os.getenv("BRANCH_NAME")

def update_github_variable(variable_name, new_value):
    #GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    # GitHub API endpoint for updating repository variables
    api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/variables/{variable_name}"

    # Request headers
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    # Payload with the new value for the variable
    payload = {
        "name": variable_name,
        "value": new_value
    }

    # Make a PATCH request to update the variable
    response = requests.patch(api_url, headers=headers, json=payload)

    if response.status_code >= 200 and response.status_code <= 300:
        print(f"Variable '{variable_name}' updated successfully to '{new_value}'.")
    else:
        print(f"Failed to update variable. Status code: {response.status_code}")
        print(f"Response: {response.text}")

def read_github_variable(variable_name):
    #GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    # GitHub API endpoint for updating repository variables
    api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/variables/{variable_name}"

    # Request headers
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code >= 200 and response.status_code <= 300:
        print(f"Variable '{variable_name}' read successfully, value = {response.json().get('value')}.")
        return response.json().get("value")
    else:
        print(f"Failed to read variable {variable_name}. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return "error"

def update_publish_at(prevouse_publish_at):
    # Parse the publish_at timestamp
    #publish_at = "2025-01-07T22:00:00Z"  # Example input
    publish_at = prevouse_publish_at  # Example input
    time = datetime.fromisoformat(publish_at.replace("Z", "+00:00"))

    print(f"{time.isoformat()} hour {time.hour}")
    # Adjust time based on the hour
    if time.hour == 22:
        time += timedelta(hours=15)
    else:
        time += timedelta(hours=9)
    print(f"{time.isoformat()} hour {time.hour}")

    update_github_variable(f"{BRANCH_NAME}_PUBLISH_AT", time.isoformat())

    print("Publish time successfully updated on GitHub!")

def load_credentials():
    """Load credentials from a JSON file."""
    with open("token.pickle", "r") as f:
        data = json.load(f)
    client_id = data["client_id"]
    print(f"Data '{data}' received '{client_id}'.")
    return Credentials(
        token=data["token"],
        refresh_token=data["refresh_token"],
        client_id=data["client_id"],
        client_secret=data["client_secret"],
        token_uri=data["token_uri"]
    )

def upload_video_to_youtube(title, description, video_path, thumbnail_path, publish_at):
    """Upload a video to YouTube."""
    # Load credentials
    with open('token.pickle', 'rb') as token:
        #with open('token.pickle', 'rb') as token:
        credentials = load_credentials()

    # Build the YouTube API client
    youtube = build('youtube', 'v3', credentials=credentials)

    # Video metadata
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            #'tags': [title.split(" ").first, title.split(" ").last, description.split(" ").last],
            'categoryId': 22,
            #'channel_id': read_file(CHANNEL_ID_FILE),
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': publish_at,
            'madeForKids': False,
            'selfDeclaredMadeForKids': False,
        }
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
    if 'id' in response:
        print(f"Video uploaded: {response['id']}")

        # Upload thumbnail
        print(f"Uploading thumbnail: {thumbnail_path}")
        youtube.thumbnails().set(
            videoId=response['id'],
            media_body=MediaFileUpload(thumbnail_path)
        ).execute()
        print(f"Thumbnail uploaded.")
        update_publish_at(publish_at)
    else:
        print("Video upload failed, no ID in response.")

if __name__ == "__main__":
    # Read metadata from files
    title = read_file(TITLE_FILE)
    description = read_file(DESCRIPTION_FILE)
    video_link = read_file(VIDEO_LINK_FILE)
    thumbnail_link = read_file(THUMBNAIL_LINK_FILE)
    publish_at = read_github_variable(f"{BRANCH_NAME}_PUBLISH_AT")

    # Download video and thumbnail
    download_file(video_link, VIDEO_FILE)
    download_file(thumbnail_link, THUMBNAIL_FILE)

    # Upload video to YouTube
    upload_video_to_youtube(title, description, VIDEO_FILE, THUMBNAIL_FILE, publish_at)
