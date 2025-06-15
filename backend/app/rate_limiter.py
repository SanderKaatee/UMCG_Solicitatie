# app/rate_limiter.py
import redis
import time
from typing import Optional
from app.config import Config

class RateLimiter:
    """Token bucket rate limiter using Redis"""
    
    def __init__(self):
        self.redis_client = redis.from_url(Config.REDIS_URL)
        self.requests_limit = Config.RATE_LIMIT_REQUESTS
        self.window = Config.RATE_LIMIT_WINDOW
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed based on rate limit"""
        key = f"rate_limit:{identifier}"
        current_time = int(time.time())
        window_start = current_time - self.window
        
        pipe = self.redis_client.pipeline()
        
        # Remove old entries
        pipe.zremrangebyscore(key, 0, window_start)
        
        # Count current requests in window
        pipe.zcard(key)
        
        # Add current request
        pipe.zadd(key, {str(current_time): current_time})
        
        # Set expiry
        pipe.expire(key, self.window)
        
        results = pipe.execute()
        request_count = results[1]
        
        return request_count < self.requests_limit
    
    def get_reset_time(self, identifier: str) -> Optional[int]:
        """Get the time when rate limit resets"""
        key = f"rate_limit:{identifier}"
        oldest = self.redis_client.zrange(key, 0, 0, withscores=True)
        
        if oldest:
            return int(oldest[0][1]) + self.window
        return None