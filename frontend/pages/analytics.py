import streamlit as st
from services.api_client import api_client
from components.analytics_components import (
    analytics_metrics, click_timeline_chart, 
    top_countries_chart, top_referrers_chart,
    global_analytics_summary, top_urls_table
)

st.set_page_config(page_title="Analytics - Links from Liliput", page_icon="📈")

st.title("📈 Liliput Analytics Kingdom")

# Themed header
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; color: white;'>
    <h2>🔮 Crystal Ball Analytics</h2>
    <p style='margin: 0; opacity: 0.9;'>Peer into the magical realm of your link performance</p>
</div>
""", unsafe_allow_html=True)

# Tabs for different analytics views
tab1, tab2 = st.tabs(["🌐 Kingdom Overview", "🔍 Individual Link Sorcery"])

with tab1:
    st.subheader("🏰 Kingdom-Wide Analytics")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("*Discover the grand patterns across all your tiny links*")
    with col2:
        if st.button("🔄 Refresh Crystal Ball", type="primary"):
            st.cache_data.clear()
            st.rerun()
    
    # Fetch global analytics
    with st.spinner("🔮 Consulting the crystal ball..."):
        global_data = api_client.get_global_analytics()
    
    if global_data:
        # Global metrics with Liliput theming
        st.markdown("### 👑 Royal Statistics")
        global_analytics_summary(global_data)
        
        st.markdown("---")
        
        # Top performing links
        if 'top_urls' in global_data and global_data['top_urls']:
            st.markdown("### 🏆 Champion Links of the Realm")
            top_urls_table(global_data['top_urls'])
        else:
            st.markdown("""
            <div style='text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 10px; border: 2px dashed #dee2e6;'>
                <h3>🏰 Your Kingdom Awaits!</h3>
                <p>Create some tiny links to see the magic of analytics unfold</p>
                <p><em>Every great journey starts with a single link...</em></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("❌ The crystal ball is cloudy - could not load kingdom analytics")

with tab2:
    st.subheader("🔮 Individual Link Divination")
    
    # Enhanced URL input with Liliput styling
    st.markdown("*Cast a spell to reveal the secrets of any specific link*")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        short_code = st.text_input(
            "🪄 Enter the magical code:", 
            placeholder="abc123",
            help="Enter your link's short code to divine its performance"
        )
    with col2:
        analyze_btn = st.button("🔮 Cast Analytics Spell", use_container_width=True)
    
    if analyze_btn and short_code:
        with st.spinner(f"✨ Weaving analytics magic for /{short_code}..."):
            analytics = api_client.get_url_analytics(short_code)
        
        if analytics:
            st.success(f"🎯 Divination complete for /{short_code}")
            
            # Link performance overview
            st.markdown("### 📊 Performance Enchantment")
            analytics_metrics(analytics)
            
            st.markdown("---")
            
            # Charts section with magical theming
            st.markdown("### 📈 Visual Spells & Incantations")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if analytics.get('click_timeline'):
                    st.markdown("#### ⏰ Time Travel Chronicles")
                    click_timeline_chart(analytics['click_timeline'])
                else:
                    st.info("🕰️ No time chronicles available yet")
            
            with col2:
                if analytics.get('top_countries'):
                    st.markdown("#### 🗺️ Realm Exploration Map")
                    top_countries_chart(analytics['top_countries'])
                else:
                    st.info("🌍 No realm exploration data yet")
            
            # Traffic sources
            if analytics.get('top_referers'):
                st.markdown("#### 🚪 Magical Portals (Traffic Sources)")
                top_referrers_chart(analytics['top_referers'])
            else:
                st.info("🚪 No portal data discovered yet")
                
            # Additional insights
            st.markdown("---")
            st.markdown("### 🧙‍♂️ Wizard's Insights")
            
            if analytics['total_clicks'] > 0:
                unique_rate = (analytics['unique_clicks'] / analytics['total_clicks']) * 100
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "🎭 Uniqueness Spell", 
                        f"{unique_rate:.1f}%",
                        help="Percentage of unique visitors"
                    )
                with col2:
                    avg_daily = analytics['total_clicks'] / max(1, (analytics.get('days_active', 1)))
                    st.metric(
                        "⚡ Daily Magic Power", 
                        f"{avg_daily:.1f}",
                        help="Average clicks per day"
                    )
                with col3:
                    growth_indicator = "📈" if analytics['clicks_today'] > 0 else "📊"
                    st.metric(
                        f"{growth_indicator} Today's Energy", 
                        analytics['clicks_today'],
                        help="Clicks received today"
                    )
            else:
                st.info("✨ This link is waiting for its first magical interaction!")
                
        else:
            st.error("🌙 The spell failed - could not divine analytics for this link code")

# Magical footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1rem; color: #666; font-style: italic;'>
    ✨ <em>Analytics magic powered by the wisdom of Liliput's finest data wizards</em> ✨
</div>
""", unsafe_allow_html=True)
