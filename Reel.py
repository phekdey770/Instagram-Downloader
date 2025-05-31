import instaloader

def download_reels(username):
    L = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        for post in profile.get_posts():
            if post.typename == "GraphVideo" and post.is_video and post.video_url:
                L.download_post(post, target=profile.username)
                print(f"Reel downloaded: {post.url}")
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile with username '{username}' does not exist.")

if __name__ == "__main__":
    username = "molykaa__shop2"
    download_reels(username)
