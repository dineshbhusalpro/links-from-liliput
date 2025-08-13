import requests
import streamlit as st
from typing import Dict, Any, Optional
from config.settings import API_ENDPOINTS

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 10
    
    def _make_request(self, method: str, url: str, **kwargs) -> Optional[Dict[Any, Any]]:
        """Make API request with error handling"""
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            return None
    
    def create_short_url(self, original_url: str, custom_code: str = None) -> Optional[Dict]:
        """Create a shortened URL"""
        payload = {"original_url": original_url}
        if custom_code:
            payload["custom_code"] = custom_code
        
        return self._make_request("POST", API_ENDPOINTS["SHORTEN_URL"], json=payload)
    
    def get_url_stats(self, short_code: str) -> Optional[Dict]:
        """Get URL statistics"""
        return self._make_request("GET", API_ENDPOINTS["URL_STATS"](short_code))
    
    def get_url_analytics(self, short_code: str) -> Optional[Dict]:
        """Get URL analytics"""
        return self._make_request("GET", API_ENDPOINTS["ANALYTICS"](short_code))
    
    def get_global_analytics(self) -> Optional[Dict]:
        """Get global analytics"""
        return self._make_request("GET", API_ENDPOINTS["GLOBAL_ANALYTICS"])
    
    def check_health(self) -> Optional[Dict]:
        """Check API health"""
        return self._make_request("GET", API_ENDPOINTS["HEALTH"])

# Create singleton instance
api_client = APIClient()
