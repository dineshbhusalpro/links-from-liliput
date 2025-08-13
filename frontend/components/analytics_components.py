import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from services.utils import format_number, create_timeline_df

def analytics_metrics(analytics_data: dict):
    """Display analytics metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🖱️ Total Clicks",
            value=format_number(analytics_data.get('total_clicks', 0))
        )
    
    with col2:
        st.metric(
            label="👥 Unique Visitors",
            value=format_number(analytics_data.get('unique_clicks', 0))
        )
    
    with col3:
        st.metric(
            label="📅 Today",
            value=format_number(analytics_data.get('clicks_today', 0))
        )
    
    with col4:
        st.metric(
            label="📊 This Month",
            value=format_number(analytics_data.get('clicks_this_month', 0))
        )

def click_timeline_chart(timeline_data: list):
    """Display click timeline chart"""
    if not timeline_data:
        st.info("No timeline data available")
        return
    
    df = create_timeline_df(timeline_data)
    
    fig = px.line(
        df, 
        x='date', 
        y='clicks',
        title='📈 Click Timeline',
        labels={'clicks': 'Number of Clicks', 'date': 'Date'}
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Clicks",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def top_countries_chart(countries_data: list):
    """Display top countries chart"""
    if not countries_data:
        st.info("No country data available")
        return
    
    df = pd.DataFrame(countries_data)
    
    fig = px.bar(
        df, 
        x='count', 
        y='name',
        orientation='h',
        title='🌍 Top Countries',
        labels={'count': 'Clicks', 'name': 'Country'}
    )
    
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

def top_referrers_chart(referrers_data: list):
    """Display top referrers pie chart"""
    if not referrers_data:
        st.info("No referrer data available")
        return
    
    df = pd.DataFrame(referrers_data)
    
    fig = px.pie(
        df, 
        values='count', 
        names='name',
        title='🔗 Traffic Sources'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def global_analytics_summary(global_data: dict):
    """Display global analytics summary"""
    st.subheader("🌐 Platform Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🖱️ Total Clicks",
            value=format_number(global_data.get('total_clicks', 0)),
            delta=f"+{global_data.get('clicks_today', 0)} today"
        )
    
    with col2:
        st.metric(
            label="👥 Unique Visitors",
            value=format_number(global_data.get('unique_visitors', 0))
        )
    
    with col3:
        st.metric(
            label="📅 Today's Clicks",
            value=format_number(global_data.get('clicks_today', 0))
        )
    
    with col4:
        st.metric(
            label="📊 This Week",
            value=format_number(global_data.get('clicks_this_week', 0))
        )

def top_urls_table(top_urls: list):
    """Display top URLs table"""
    if not top_urls:
        st.info("No URL data available")
        return
    
    st.subheader("🏆 Top Performing URLs")
    
    df = pd.DataFrame(top_urls)
    df.index = df.index + 1  # Start from 1
    df['short_code'] = df['short_code'].apply(lambda x: f"/{x}")
    
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "short_code": "Short URL",
            "clicks": st.column_config.NumberColumn(
                "Clicks",
                format="%d"
            )
        }
    )
