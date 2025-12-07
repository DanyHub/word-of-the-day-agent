from scraper import fetch_word_of_the_day
from storage import save_word
from notifier import send_daily_word
import datetime
import os

def main():
    print(f"Starting daily job at {datetime.datetime.now()}")
    
    # 1. Fetch
    word_data = fetch_word_of_the_day()
    if not word_data:
        print("Failed to fetch word. Exiting.")
        return

    # 2. Save
    saved = save_word(word_data)
    if saved:
        print(f"New word saved: {word_data['word']}")
    else:
        print(f"Word '{word_data['word']}' already exists in history.")

    # 3. Notify
    # Only notify if it's a new word OR if we want to force it. 
    # Usually for reliable daily updates, we might want to send it even if saved previously 
    # (in case the previous run failed to notify), but strictly speaking we only notify on new.
    # However, for simplicity and robustness, let's notify if we have data.
    # But to avoid spamming on re-runs, let's stick to the logic: "If we fetched it today, show it."
    
    if send_daily_word(word_data):
        print("Notification sent.")
    else:
        print("Failed to send notification.")

if __name__ == "__main__":
    main()
