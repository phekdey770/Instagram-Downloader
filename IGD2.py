import instaloader
import os
import shutil
from concurrent.futures import ThreadPoolExecutor

# Define parameters
username = "sivly_samnang"  # The desired Instagram username
base_path = "D:/TEST 2/Data/IG/"  # The base path for saving content

# Create a folder for the specified Instagram user
user_path = os.path.join(base_path, username)  # The main folder for the user
img_path = os.path.join(user_path, "IMG")  # Subfolder for images
vdo_path = os.path.join(user_path, "VDO")  # Subfolder for videos
profile_path = os.path.join(user_path, "PROFILE")  # Subfolder for profile picture
other_path = os.path.join(user_path, "OTHER")  # Subfolder for other files

# Ensure all necessary folders exist
for path in [user_path, img_path, vdo_path, profile_path, other_path]:
    if not os.path.exists(path):
        os.makedirs(path)

# Function to download photos
def download_photos():
    loader = instaloader.Instaloader(
        download_pictures=True,
        download_video_thumbnails=True,
        download_geotags=False,
        download_comments=False,
        save_metadata=True,
        dirname_pattern=user_path,  # Base path for content
        filename_pattern="{date_utc}_{profile}",  # Filename pattern
    )
    loader.download_profile(username, profile_pic_only=False)

# Function to download videos
def download_videos():
    loader = instaloader.Instaloader(
        download_pictures=False,
        download_videos=True,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=True,
        dirname_pattern=user_path,  # Base path for content
        filename_pattern="{date_utc}_{profile}",  # Filename pattern
    )
    loader.download_profile(username, profile_pic_only=False)

# Download photos and videos concurrently
with ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(download_photos)
    executor.submit(download_videos)

# Move files with 'profile' in the name to 'PROFILE'
for root, _, files in os.walk(user_path):
    for file in files:
        source = os.path.join(root, file)
        if "profile" in file.lower():  # If file name contains 'profile'
            destination = os.path.join(profile_path, file)  # Move to 'PROFILE'
            shutil.move(source, destination)
        elif file.endswith((".mp4", ".mov", ".mkv", ".avi")):
            destination = os.path.join(vdo_path, file)  # Move to 'VDO'
            shutil.move(source, destination)
        elif file.endswith((".jpg", ".jpeg", ".png")):
            destination = os.path.join(img_path, file)  # Move to 'IMG'
            shutil.move(source, destination)
        else:
            destination = os.path.join(other_path, file)  # Move to 'OTHER'
            shutil.move(source, destination)

# Delete 'OTHER' folder, regardless of its contents
if os.path.exists(other_path):  # If 'OTHER' folder exists
    shutil.rmtree(other_path)  # Recursively delete 'OTHER' folder and its contents
