import os
import instaloader

def download_user_posts(username):
    # Create a directory for the user if it doesn't exist
    user_folder = f"{username}_ig"
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    # Initialize Instaloader
    L = instaloader.Instaloader()

    # Download user's posts
    profile = instaloader.Profile.from_username(L.context, username)
    post_urls = []
    for post in profile.get_posts():
        if not post.is_video:  # Only download pictures
            L.download_post(post, target=user_folder)
            post_urls.append(f"https://www.instagram.com/p/{post.shortcode}/")

    return post_urls

def move_files(source_folder, destination_folder):
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        destination_path = os.path.join(destination_folder, filename)
        os.replace(source_path, destination_path)

def download_photos_by_id(post_urls):
    # Initialize Instaloader
    L = instaloader.Instaloader()

    # Create directories for images and videos
    image_folder = 'Image'
    video_folder = 'Video'
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    for url in post_urls:
        post_id = url.split('/')[-2]  # Extract post ID from URL
        post = instaloader.Post.from_shortcode(L.context, post_id)
        if not post.is_video:  # Download images
            for node in post.get_sidecar_nodes():  # Handle multiple images in one post
                if node.is_video:
                    continue
                if node.display_url.endswith('.jpg'):  # Check if the file is a JPG image
                    L.download_pic(node.display_url, os.path.join(image_folder, f"{post_id}.jpg"))
                    print(f"Downloaded photo from {url}")
                else:
                    print(f"Skipped non-JPG file from {url}")
        else:  # Download videos
            L.download_post(post, target=video_folder)
            print(f"Downloaded video from {url}")

    # Move downloaded files to appropriate folders
    move_files(username + "_ig", image_folder)
    move_files(username + "_ig", video_folder)

if __name__ == "__main__":
    # Prompt the user to input the username
    username = "molykaa__shop2"

    # Download posts of the specified user and get post URLs
    user_post_urls = download_user_posts(username)

    # Download photos by image ID
    download_photos_by_id(user_post_urls)
