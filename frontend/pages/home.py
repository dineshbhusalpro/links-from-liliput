import streamlit as st
from components.url_components import url_shortener_form

st.set_page_config(page_title="Home - Links from Liliput", page_icon="🏠")

st.title("🏠 Links from Liliput")
st.markdown("Welcome to Links from Liliput! Create and manage your tiny links from our magical world.")

# Hero section with Liliput theme
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem; color: white;'>
    <h2>🏰 Welcome to the Land of Tiny Links!</h2>
    <p style='font-size: 1.2em; margin-bottom: 0;'>Where big URLs become delightfully small</p>
</div>
""", unsafe_allow_html=True)

# URL Shortener
result = url_shortener_form()

# Features section with Liliput theming
st.markdown("---")
st.subheader("✨ Why Choose Links from Liliput?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **⚡ Lightning Fast Magic**
    - Instant URL transformation
    - Powered by Lilliputian technology
    - Swift as Gulliver's travels
    """)

with col2:
    st.markdown("""
    **📊 Tiny Analytics, Big Insights**
    - Track every click journey
    - Geographic exploration data
    - Discover your audience's travels
    """)

with col3:
    st.markdown("""
    **🎨 Customizable & Memorable**
    - Create your own tiny codes
    - Brand your miniature links
    - Easy API for bulk adventures
    """)

# Success state with Liliput flair
if result:
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: #d4edda; border-radius: 8px; border-left: 4px solid #28a745;'>
        <h3>🎉 Your Link Has Been Shrunk to Liliput Size!</h3>
        <p>Share your tiny link and watch the magic happen ✨</p>
    </div>
    """, unsafe_allow_html=True)
