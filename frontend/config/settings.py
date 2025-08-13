import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

API_ENDPOINTS = {
    "SHORTEN_URL": f"{API_BASE_URL}/api/v1/shorten",
    "URL_STATS": lambda code: f"{API_BASE_URL}/api/v1/urls/{code}/stats",
    "ANALYTICS": lambda code: f"{API_BASE_URL}/api/v1/analytics/{code}",
    "GLOBAL_ANALYTICS": f"{API_BASE_URL}/api/v1/analytics/global",
    "HEALTH": f"{API_BASE_URL}/health/all"
}