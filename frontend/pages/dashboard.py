import streamlit as st
from services.api_client import api_client
from components.url_components import url_shortener_form, url_card

st.set_page_config(page_title="Dashboard - Links from Liliput", page_icon="📊")

st.title("📊 Liliput Dashboard")
st.markdown("Command center for all your tiny links and their adventures.")

# Liliput-themed dashboard header
st.markdown("""
<div style='background: linear-gradient(90deg, #ff9a56 0%, #ffad56 100%); padding: 1rem; border-radius: 8px; margin-bottom: 2rem;'>
    <h3 style='color: white; margin: 0;'>🏰 Link Management Palace</h3>
    <p style='color: white; margin: 0; opacity: 0.9;'>Create, monitor, and manage your collection of tiny links</p>
</div>
""", unsafe_allow_html=True)

# URL Shortener section
st.subheader("🔗 Create New Tiny Link")
result = url_shortener_form()

# Quick Stats
st.subheader("📈 Quick Kingdom Stats")
try:
    global_stats = api_client.get_global_analytics()
    if global_stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🖱️ Total Adventures", 
                value=global_stats.get('total_clicks', 0),
                help="Total clicks across all your tiny links"
            )
        with col2:
            st.metric(
                label="👥 Unique Travelers", 
                value=global_stats.get('unique_visitors', 0),
                help="Unique visitors to your links"
            )
        with col3:
            st.metric(
                label="📅 Today's Journeys", 
                value=global_stats.get('clicks_today', 0),
                help="Clicks received today"
            )
        with col4:
            st.metric(
                label="📊 Weekly Expeditions", 
                value=global_stats.get('clicks_this_week', 0),
                help="Clicks this week"
            )
except Exception as e:
    st.warning("Unable to load kingdom statistics at the moment.")

# Link Management Section
st.subheader("🔍 Explore Individual Link")

col1, col2 = st.columns([2, 1])
with col1:
    short_code = st.text_input(
        "Enter your tiny link code:", 
        placeholder="abc123",
        help="Enter the short code (without the domain) to view its details"
    )
with col2:
    if st.button("🔍 Investigate Link", use_container_width=True):
        if short_code:
            with st.spinner("Investigating your tiny link..."):
                stats = api_client.get_url_stats(short_code)
            
            if stats:
                st.success("✅ Link found in our records!")
                
                # Enhanced URL card display
                with st.container():
                    st.markdown("### 📋 Link Details")
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"**🔗 Short Code:** `{stats['short_code']}`")
                        st.markdown(f"**🌐 Original URL:** {stats['original_url']}")
                        st.markdown(f"**📅 Created:** {stats['created_at'][:10]}")
                    
                    with col2:
                        status_color = "🟢" if stats['is_active'] else "🔴"
                        st.markdown(f"**Status:** {status_color} {'Active' if stats['is_active'] else 'Inactive'}")
                        st.metric("Adventure Count", stats['click_count'])
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📊 View Analytics", key="analytics_btn"):
                        st.switch_page("pages/analytics.py")
                with col2:
                    if st.button("📋 Copy Link", key="copy_btn"):
                        st.success("✅ Link copied! (Use your browser's copy function)")
                with col3:
                    short_url = f"http://localhost/{stats['short_code']}"
                    st.markdown(f"[🔗 Visit Link]({short_url})")
                        
            else:
                st.error("❌ No link found with that code. Check your spelling or create a new link!")

# Instructions for future enhancements
st.markdown("---")
st.info("""
💡 **Enhancement Ideas:**
- Add a "My Links" section by implementing a user system
- Bulk URL creation from CSV files
- Link expiration settings
- Custom domains support
""")
