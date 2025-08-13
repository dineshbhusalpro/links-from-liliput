import streamlit as st
from services.api_client import api_client
from services.utils import validate_url, validate_custom_code

def url_shortener_form():
    """URL shortener form component"""
    st.subheader("Shorten Your URL")
    
    with st.form("url_shortener", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            original_url = st.text_input(
                "Enter URL to shorten:", 
                placeholder="https://example.com",
                help="Enter a valid URL starting with http:// or https://"
            )
        
        with col2:
            custom_code = st.text_input(
                "Custom code (optional):", 
                placeholder="my-code",
                help="3-20 characters, letters, numbers, hyphens, underscores"
            )
        
        submitted = st.form_submit_button("Shorten URL", use_container_width=True)
        
        if submitted:
            # Validation
            if not original_url:
                st.error("Please enter a URL")
                return None
            
            if not validate_url(original_url):
                st.error("Please enter a valid URL (must start with http:// or https://)")
                return None
            
            if custom_code and not validate_custom_code(custom_code):
                st.error("Custom code must be 3-20 characters and contain only letters, numbers, hyphens, and underscores")
                return None
            
            # Create short URL
            with st.spinner("Creating short URL..."):
                result = api_client.create_short_url(original_url, custom_code)
            
            if result:
                st.success("✅ URL shortened successfully!")
                
                # Display result
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.code(result['short_url'], language=None)
                with col2:
                    st.info("Use Ctrl+C to copy from the code box")
                    # if st.button("📋 Copy", key="copy_btn"):
                    #     st.balloons()
                    #     st.info("URL copied! (Use Ctrl+C to copy from the code box)")
                
                # Display details
                with st.expander("📊 URL Details", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Short Code", result['short_code'])
                    col2.metric("Clicks", result['click_count'])
                    col3.metric("Status", "Active" if result['is_active'] else "Inactive")
                
                return result
    
    return None

def url_card(url_data: dict):
    """Display URL information card"""
    with st.container():
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**Short Code:** `{url_data['short_code']}`")
            st.markdown(f"**Original URL:** {url_data['original_url'][:50]}...")
        
        with col2:
            st.metric("Clicks", url_data['click_count'])
        
        with col3:
            status = "🟢 Active" if url_data['is_active'] else "🔴 Inactive"
            st.markdown(f"**Status:** {status}")
