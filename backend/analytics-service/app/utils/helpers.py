import re
from typing import Optional, Dict
from user_agents import parse
import requests
import logging

logger = logging.getLogger(__name__)

def extract_user_info(user_agent_string: str) -> Dict[str, str]:
    """Extract browser and OS information from user agent"""
    try:
        user_agent = parse(user_agent_string)
        return {
            "browser": f"{user_agent.browser.family} {user_agent.browser.version_string}",
            "os": f"{user_agent.os.family} {user_agent.os.version_string}",
            "device": user_agent.device.family
        }
    except Exception as e:
        logger.error(f"Error parsing user agent: {e}")
        return {"browser": "Unknown", "os": "Unknown", "device": "Unknown"}

def get_country_from_ip(ip_address: str) -> Optional[str]:
    """Get country code from IP address (simple implementation)"""
    # This is a basic implementation
    # In production, use services like MaxMind GeoIP2 or ip-api.com
    try:
        if ip_address in ["127.0.0.1", "localhost", "::1"]:
            return "Nepal"  # Default for localhost
        
        # You could implement actual IP geolocation here
        # For now, return None to keep it simple
        return None
    except Exception as e:
        logger.error(f"Error getting country from IP {ip_address}: {e}")
        return None