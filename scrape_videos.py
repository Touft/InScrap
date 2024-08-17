import os
import time
import instaloader
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
import threading
from datetime import datetime, timedelta, timezone

console = Console()

def authenticate(username, password):
    """
    Authenticate to Instagram and return the Instaloader instance.
    """
    console.print(f"Authenticating user {username}...", style="bold blue")
    L = instaloader.Instaloader()

    try:
        L.load_session_from_file(username)
        console.print("Session loaded from file.", style="bold green")
    except FileNotFoundError:
        console.print("No session found. Logging in...", style="bold yellow")
        L.login(username, password)
        L.save_session_to_file()
        console.print("Session saved to file.", style="bold green")

    return L

def get_followed_profiles(L):
    """
    Retrieve the profiles followed by the user.
    """
    profile = instaloader.Profile.from_username(L.context, L.test_login())
    following = list(profile.get_followees())
    console.print(f"{len(following)} followed accounts found.", style="bold blue")
    return following

def download_posts_from_profile(L, profile, since_date, output_folder, stop_event, progress):
    """
    Download posts from a profile since a given date.
    """
    console.print(f"Downloading from account: {profile.username}", style="bold blue")
    start_time = time.time()
    time_limit = 30

    count = 0
    for post in profile.get_posts():
        if stop_event.is_set():
            console.print(f"Download interrupted for account: {profile.username}.", style="bold yellow")
            break

        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            console.print(f"Time limit reached for account: {profile.username}. Moving to the next account.", style="bold yellow")
            break

        post_date = post.date_utc.replace(tzinfo=timezone.utc)
        if since_date <= post_date:
            if post.is_video or post.typename == 'GraphVideo':
                L.download_post(post, target=output_folder)
                count += 1
                console.print(f"Post downloaded: {post.shortcode}", style="bold green")

            if count >= 30:
                console.print(f"Download limit reached for account: {profile.username}.", style="bold yellow")
                break

def scrapeVideos(username, password, output_folder, days, stop_event):
    """
    Main function for scraping and downloading videos.
    """
    try:
        L = authenticate(username, password)

        since_date = datetime.now(timezone.utc) - timedelta(days=days)
        console.print(f"Posts since: {since_date}", style="bold blue")

        following = get_followed_profiles(L)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            console.print(f"Output directory created: {output_folder}", style="bold green")

        with Progress(SpinnerColumn(), BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"), console=console) as progress:
            for profile in following:
                download_posts_from_profile(L, profile, since_date, output_folder, stop_event, progress)
        
        console.print("Download completed.", style="bold green")
    
    except Exception as e:
        console.print(f"Error during video scraping: {e}", style="bold red")
