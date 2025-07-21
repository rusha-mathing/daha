import time
from typing import Dict, Any
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio

class MetricsCollector:
    def __init__(self):
        self.request_counts = defaultdict(int)
        self.response_times = defaultdict(list)
        self.error_counts = defaultdict(int)
        self.start_time = datetime.utcnow()

    def record_request(self, endpoint: str, method: str, status_code: int, response_time: float):
        """Record a request metric"""
        key = f"{method} {endpoint}"
        self.request_counts[key] += 1
        
        if status_code >= 400:
            self.error_counts[key] += 1
        
        self.response_times[key].append(response_time)
        
        # Keep only last 1000 response times per endpoint
        if len(self.response_times[key]) > 1000:
            self.response_times[key] = self.response_times[key][-1000:]

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        uptime = datetime.utcnow() - self.start_time
        
        # Calculate averages
        avg_response_times = {}
        for key, times in self.response_times.items():
            if times:
                avg_response_times[key] = sum(times) / len(times)

        return {
            "uptime_seconds": uptime.total_seconds(),
            "total_requests": sum(self.request_counts.values()),
            "request_counts": dict(self.request_counts),
            "error_counts": dict(self.error_counts),
            "avg_response_times": avg_response_times,
            "timestamp": datetime.utcnow().isoformat()
        }

    def reset(self):
        """Reset all metrics"""
        self.request_counts.clear()
        self.response_times.clear()
        self.error_counts.clear()
        self.start_time = datetime.utcnow()

# Global metrics collector
metrics = MetricsCollector()

class MetricsMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.time()
        
        # Create a custom send function to capture response
        async def send_with_metrics(message):
            if message["type"] == "http.response.start":
                # Record metrics after response is sent
                response_time = time.time() - start_time
                method = scope["method"]
                path = scope["path"]
                status = message.get("status", 500)
                
                metrics.record_request(path, method, status, response_time)
            
            await send(message)

        await self.app(scope, receive, send_with_metrics) 