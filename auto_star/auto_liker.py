import time
import logging
import requests
from typing import List, Dict, Optional, Tuple
from datetime import datetime

class AutoLiker:
    def __init__(self, username: str, password: str, bark_key: Optional[str] = None):
        self.username = username
        self.password = password
        self.bark_key = bark_key
        self.base_url = "https://api.appsdev.cc"
        self.access_token = None
        self.headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': 'api.appsdev.cc',
            'Connection': 'keep-alive'
        }
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def send_bark_notification(self, title: str, message: str) -> None:
        """Send notification via Bark."""
        if not self.bark_key:
            return
            
        try:
            url = f"https://api.day.app/{self.bark_key}/{title}/{message}"
            requests.get(url, timeout=5)
        except Exception as e:
            self.logger.error(f"Failed to send Bark notification: {e}")

    def login(self) -> bool:
        """Login and get access token."""
        try:
            response = requests.get(
                f"{self.base_url}/?s=App.Github_Index.Login",
                headers=self.headers,
                json={
                    "username": self.username,
                    "password": self.password
                }
            )
            
            data = response.json()
            if data.get('code') != 200 or not data.get('data', {}).get('access_token'):
                error_msg = f"Login failed: {data.get('msg', 'Unknown error')}"
                self.logger.error(error_msg)
                self.send_bark_notification("Login Failed", error_msg)
                return False
                
            self.access_token = data['data']['access_token']
            self.headers['x-access-token'] = self.access_token
            self.logger.info("Successfully logged in")
            self.send_bark_notification("Login Success", "AutoLiker login successful")
            return True
                
        except Exception as e:
            error_msg = f"Error during login: {e}"
            self.logger.error(error_msg)
            self.send_bark_notification("Login Error", error_msg)
            return False

    def get_repositories(self, page: int = 1) -> List[Dict]:
        """Get list of repositories."""
        try:
            response = requests.get(
                f"{self.base_url}/?s=App.Github_Index.Praise",
                headers=self.headers,
                json={
                    "pageNum": page,
                    "pageSize": 20,
                    "type": 1
                }
            )
            
            data = response.json()
            if data.get('code') != 200:
                self.logger.error(f"Error fetching repositories: {data.get('msg')}")
                return []
                
            repos = data.get('data', {}).get('list', [])
            self.logger.info(f"Found {len(repos)} repositories on page {page}")
            return repos
            
        except Exception as e:
            self.logger.error(f"Error fetching repositories: {e}")
            return []

    def like_repository(self, uid: int, rid: int) -> bool:
        """Like a specific repository."""
        try:
            response = requests.get(
                f"{self.base_url}/?s=App.Github_Processor.giveALike",
                headers=self.headers,
                json={
                    "uid": uid,
                    "rid": rid,
                    "type": 1
                }
            )
            
            data = response.json()
            
            # Check if already liked
            if data.get('code') == 10000 and "Duplicate entry" in data.get('msg', ''):
                self.logger.info(f"Repository {rid} was already liked, skipping")
                return True, False
                
            # Check for rate limit
            if "点赞失败, 1小时超过5次限制" in data.get('msg', ''):
                self.logger.warning("Rate limit reached (5 likes per hour)")
                self.send_bark_notification("Rate Limit", "Reached 5 likes per hour limit")
                return False, True 
                
            if data.get('code') != 200:
                self.logger.error(f"Error liking repository {rid}: {data.get('msg')}")
                return False, False
                
            self.logger.info(f"Successfully liked repository {rid} (uid: {uid})")
            return True, False
            
        except Exception as e:
            self.logger.error(f"Error liking repository {rid}: {e}")
            return False, False

    def run_once(self) -> int:
        """Run a single iteration of the auto-liker.
        Returns the number of successful likes in this run.
        """
        if not self.login():
            return 0

        likes_count = 0
        page = 1
        
        while likes_count < 5:
            repositories = self.get_repositories(page)
            if not repositories:
                break
                
            for repo in repositories:
                if not repo.get('uid') or not repo.get('rid'):
                    continue
                    
                success, rate_limited = self.like_repository(repo['uid'], repo['rid'])
                if success:
                    likes_count += 1
                    msg = f"Liked: {repo.get('name', 'Unknown')} (Stars: {repo.get('star_count', 'N/A')})"
                    self.logger.info(msg)
                    self.send_bark_notification("Liked", msg)
                if rate_limited:
                    break
                    

                if likes_count >= 5:
                    break
                    
                time.sleep(5)  # Small delay between likes
                
            page += 1

            if rate_limited:
                break
            
        return likes_count 