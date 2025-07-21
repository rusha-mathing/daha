import asyncio
import time
from typing import Any, Optional, Dict
from functools import wraps

class SimpleCache:
    def __init__(self, default_ttl: int = 300):
        self._cache: Dict[str, tuple] = {}
        self._default_ttl = default_ttl
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        async with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if time.time() - timestamp < self._default_ttl:
                    return value
                else:
                    del self._cache[key]
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        async with self._lock:
            self._cache[key] = (value, time.time())
            if ttl:
                # Schedule cleanup
                asyncio.create_task(self._cleanup_key(key, ttl))

    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]

    async def clear(self) -> None:
        """Clear all cache"""
        async with self._lock:
            self._cache.clear()

    async def _cleanup_key(self, key: str, ttl: int) -> None:
        """Cleanup expired key"""
        await asyncio.sleep(ttl)
        await self.delete(key)

    def size(self) -> int:
        """Get cache size"""
        return len(self._cache)

# Global cache instance
cache = SimpleCache()

def cached(ttl: int = 300):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items()))}"
            
            # Try to get from cache
            cached_value = await cache.get(key)
            if cached_value is not None:
                return cached_value
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache.set(key, result, ttl)
            return result
        return wrapper
    return decorator 