# Instagram Video Scraper Bot

This project is an Instagram Video Scraper Bot that automates the process of downloading videos from Instagram profiles that a user follows. The bot also includes a graphical user interface (GUI) built with Tkinter and a scheduling system for daily automated scrapes.

## Features

- **Graphical User Interface (GUI):** Built with Tkinter for user-friendly interaction.
- **Instagram Authentication:** Handles Instagram login and session management using `instaloader`.
- **Automated Video Downloading:** Downloads videos from followed Instagram profiles.
- **Progress Display:** Uses `rich` to show progress bars and console output.
- **Daily Scheduling:** Automatically runs the bot daily at a scheduled time using `schedule`. (BROKEN ATM :/)

##DISCLAMER
Important Notice:

While this bot is designed to automate the process of downloading videos from Instagram, there are risks associated with using it, especially when running it continuously for long periods.

Instagram Account Risks:

Account Warnings: Running the bot for extended periods of time (e.g., 8-9 hours nonstop) may trigger Instagram's anti-bot mechanisms. Users have reported receiving account warnings after prolonged usage.
Captcha Challenges: Instagram may also present Captcha challenges, requiring manual intervention to continue using the account.
Temporary Bans: In some cases, repeated scraping activity could lead to a temporary or permanent ban of the Instagram account.
Use at Your Own Risk:

This tool is provided for educational purposes, and we cannot guarantee the safety of your Instagram account.
To minimize the risk, avoid running the bot continuously for long periods and use it responsibly.
By using this bot, you acknowledge and accept these risks.

## Installation

### Prerequisites

- Python 3.6 or later

### Clone the Repository

```bash
git clone https://github.com/yourusername/instagram-video-scraper-bot.git
cd instagram-video-scraper-bot
