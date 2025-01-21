import os
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .auto_liker import AutoLiker

def run_task(liker: AutoLiker):
    """Execute one round of auto-liking."""
    likes = liker.run_once()
    print(f"Auto-liker finished with {likes} successful likes")
    return likes

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get credentials from environment variables
    username = os.getenv('GITHUB_USERNAME')
    password = os.getenv('GITHUB_PASSWORD')
    bark_key = os.getenv('BARK_KEY')
    
    if not username or not password:
        print("Error: GITHUB_USERNAME and GITHUB_PASSWORD must be set in environment variables")
        return 1
        
    # Create auto liker instance
    liker = AutoLiker(username=username, password=password, bark_key=bark_key)
    
    # Create scheduler
    scheduler = BlockingScheduler()
    
    # Run immediately when starting
    run_task(liker)
    
    # Schedule the task to run every 65 minutes
    scheduler.add_job(
        run_task,
        IntervalTrigger(minutes=65),  # Run every 65 minutes
        args=[liker],
        id='auto_liker',
        name='GitHub Auto Liker'
    )
    
    print("Starting scheduler. Task will run every 65 minutes. Press Ctrl+C to exit.")
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("\nStopping scheduler...")
        scheduler.shutdown()
        
    return 0

if __name__ == '__main__':
    exit(main()) 