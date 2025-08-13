import validators
import streamlit as st
from datetime import datetime
import pandas as pd

def validate_url(url: str) -> bool:
    """Validate URL format"""
    try:
        return validators.url(url)
    except:
        return False

def validate_custom_code(code: str) -> bool:
    """Validate custom code format"""
    if not code:
        return True  # Optional field
    if len(code) < 3 or len(code) > 20:
        return False
    return code.replace('-', '').replace('_', '').isalnum()

def format_number(num: int) -> str:
    """Format large numbers"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

def copy_to_clipboard_js(text: str):
    """Generate JavaScript for copying to clipboard"""
    return f"""
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText('{text}').then(function() {{
            alert('Copied to clipboard!');
        }});
    }}
    </script>
    <button onclick="copyToClipboard()" style="
        background-color: #1f77b4; 
        color: white; 
        border: none; 
        padding: 5px 10px; 
        border-radius: 3px; 
        cursor: pointer;
    ">📋 Copy</button>
    """

def create_timeline_df(timeline_data: list) -> pd.DataFrame:
    """Convert timeline data to DataFrame"""
    if not timeline_data:
        return pd.DataFrame(columns=['date', 'clicks'])
    
    df = pd.DataFrame(timeline_data)
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values('date')
