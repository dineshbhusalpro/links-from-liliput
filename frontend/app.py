import streamlit as st
from services.api_client import api_client

# Page config
st.set_page_config(
    page_title="Links from Liliput",
    page_icon="☕︎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        padding: 1rem 0;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🏠 Links from Liliput")
    st.markdown("*Shrink your links to tiny liliputian size*")
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🧐 Quick Actions")
    
    # Health check
    if st.button("🏥 Check API Health", use_container_width=True):
        health = api_client.check_health()
        if health:
            st.success("✅ All services healthy!")
            with st.expander("Service Status"):
                for service, status in health.get('services', {}).items():
                    emoji = "✅" if status else "❌"
                    st.write(f"{emoji} {service}: {'Healthy' if status else 'Unhealthy'}")
        else:
            st.error("❌ API is not responding")
    
    st.markdown("---")
    
    # Quick stats
    st.subheader("📊 Quick Stats")
    global_data = api_client.get_global_analytics()
    if global_data:
        st.metric("Total Clicks", global_data.get('total_clicks', 0))
        st.metric("Unique Visitors", global_data.get('unique_visitors', 0))
        st.metric("Today's Clicks", global_data.get('clicks_today', 0))

# Main content area
from components.url_components import url_shortener_form

# URL Shortener Section
result = url_shortener_form()

# Show recent URL analytics if URL was just created
if result:
    st.markdown("---")
    st.subheader("📈 Quick Analytics")
    
    analytics = api_client.get_url_analytics(result['short_code'])
    if analytics:
        from components.analytics_components import analytics_metrics
        analytics_metrics(analytics)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 2rem;'>
       Dinesh Bhusal | https://github.com/dineshbhusalpro | dinesh.bhusal.pro@gmail.com
    </div>
    """, 
    unsafe_allow_html=True
)
