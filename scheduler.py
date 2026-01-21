#!/usr/bin/env python3
"""
Scheduler for posting plant score chart to Discord every Saturday.
Can be run with: python scheduler.py
Or use with cron: 0 9 * * 6 cd /home/hannah/timelapse && /home/hannah/timelapse/.venv/bin/python scheduler.py
"""

import schedule
import time
from timelapse_lib.post_plant_score import post_plant_score_to_discord

def post_weekly_report():
    """Post the plant score chart to Discord."""
    print("📊 Posting weekly plant score report to Discord...")
    post_plant_score_to_discord()

# Schedule the task for every Saturday at 9:00 AM
schedule.every().saturday.at("12:00").do(post_weekly_report)

if __name__ == "__main__":
    print("🕐 Plant score scheduler started!")
    print("📅 Weekly reports will be posted every Saturday at 09:00 AM")
    print("Press Ctrl+C to stop.")
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
