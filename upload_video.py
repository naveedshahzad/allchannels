import os
import subprocess
from datetime import datetime, timedelta
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
PUBLISH_TIME_FILE = "publish_time.txt"
VIDEO_FILE = "video.mp4"
THUMBNAIL_FILE = "thumbnail.jpg"
GITHUB_TOKEN_FILE = "gh_token.txt"

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
#GITHUB_TOKEN = "your_personal_access_token"
REPO_OWNER = "naveedshahzad"
REPO_NAME = "lifefule"
GITHUB_TOKEN = read_file(GITHUB_TOKEN_FILE)  # Your GitHub personal access token

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

    # Payload with the new value for the variable
    #payload = {
    #    "name": variable_name,
    #    "value": new_value
    #}

    # Make a PATCH request to update the variable
    response = requests.get(api_url, headers=headers)

    if response.status_code >= 200 and response.status_code <= 300:
        print(f"Variable '{variable_name}' read successfully, value = {response.json().get('value')}.")
        return response.json().get("value")
    else:
        print(f"Failed to update variable. Status code: {response.status_code}")
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

    update_github_variable("PUBLISH_AT", time.isoformat())
    ## Write the updated time to a file
    #with open("publish_time.txt", "w") as file:
    #    file.write(time.isoformat())

    ## Print the updated time
    #print(f"Updated time for next video scheduling {time.isoformat()}")

    ## GitHub Repository Details
    #REPO_PATH = "."  # Path to your local GitHub repository
    #GITHUB_TOKEN = read_file(GITHUB_TOKEN_FILE)  # Your GitHub personal access token

    ## Set Git configuration if not already set
    #os.chdir(REPO_PATH)
    #subprocess.run(["git", "config", "--global", "user.email", "naveedkpr+1@gmail.com"])
    #subprocess.run(["git", "config", "--global", "user.name", "Muhammad Naveed Shahzad"])

    ## Add changes to Git
    #subprocess.run(["git", "add", "publish_time.txt"])

    ## Commit the changes
    #commit_message = f"Update publish time: {time.isoformat()}"
    #subprocess.run(["git", "commit", "-m", commit_message])

    ## Push the changes to GitHub
    #print(f"https://{GITHUB_TOKEN}@github.com/naveedshahzad/lifefule.git")
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

    update_github_variable("PUBLISH_AT", time.isoformat())
    ## Write the updated time to a file
    #with open("publish_time.txt", "w") as file:
    #    file.write(time.isoformat())

    ## Print the updated time
    #print(f"Updated time for next video scheduling {time.isoformat()}")

    ## GitHub Repository Details
    #REPO_PATH = "."  # Path to your local GitHub repository
    #GITHUB_TOKEN = read_file(GITHUB_TOKEN_FILE)  # Your GitHub personal access token

    ## Set Git configuration if not already set
    #os.chdir(REPO_PATH)
    #subprocess.run(["git", "config", "--global", "user.email", "naveedkpr+1@gmail.com"])
    #subprocess.run(["git", "config", "--global", "user.name", "Muhammad Naveed Shahzad"])

    ## Add changes to Git
    #subprocess.run(["git", "add", "publish_time.txt"])

    ## Commit the changes
    #commit_message = f"Update publish time: {time.isoformat()}"
    #subprocess.run(["git", "commit", "-m", commit_message])

    ## Push the changes to GitHub
    #print(f"https://{GITHUB_TOKEN}@github.com/naveedshahzad/lifefule.git")
    #subprocess.run(["git", "push", "https://{GITHUB_TOKEN}@github.com/naveedshahzad/lifefule.git", "main"])

    print("Publish time successfully updated on GitHub!")

def upload_video_to_youtube(title, description, video_path, thumbnail_path, publish_at):
    """Upload a video to YouTube."""
    # Load credentials
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)

    # Build the YouTube API client
    youtube = build('youtube', 'v3', credentials=credentials)

    # Video metadata
    #request_body = {
    #    'snippet': {
    #        'title': title,
    #        'description': description,
    #        #'tags': [title.split(" ").first, title.split(" ").last, description.split(" ").last],
    #        'categoryId': 22,
    #        #channel_id: "UCPS1Y5fHLenoiRUE3JOhV8w",
    #    },
    #    'status': {
    #        'privacyStatus': 'private',
    #        'publishAt': publish_at,
    #        'madeForKids': False,
    #        'selfDeclaredMadeForKids': False,
    #    }
    #}

    ## Upload video
    #print(f"Uploading video: {video_path}")
    #media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    #video_request = youtube.videos().insert(
    #    part='snippet,status',
    #    body=request_body,
    #    media_body=media
    #)

    #response = video_request.execute()
    #print(f"Video uploaded: {response['id']}")
    update_publish_at(publish_at)
    #if 'id' in response:
    #    print(f"Video uploaded: {response['id']}")

    #    # Upload thumbnail
    #    print(f"Uploading thumbnail: {thumbnail_path}")
    #    youtube.thumbnails().set(
    #        videoId=response['id'],
    #        media_body=MediaFileUpload(thumbnail_path)
    #    ).execute()
    #    print(f"Thumbnail uploaded.")
    #    update_publish_at(publish_at)
    #else:
    #    print("Video upload failed, no ID in response.")

if __name__ == "__main__":
    # Read metadata from files
    title = read_file(TITLE_FILE)
    description = read_file(DESCRIPTION_FILE)
    video_link = read_file(VIDEO_LINK_FILE)
    thumbnail_link = read_file(THUMBNAIL_LINK_FILE)
    thumbnail_link = read_file(THUMBNAIL_LINK_FILE)
    #publish_at = read_file(PUBLISH_TIME_FILE)
    publish_at = read_github_variable("PUBLISH_AT")

    # Download video and thumbnail
    download_file(video_link, VIDEO_FILE)
    download_file(thumbnail_link, THUMBNAIL_FILE)

    # Upload video to YouTube
    upload_video_to_youtube(title, description, VIDEO_FILE, THUMBNAIL_FILE, publish_at)
