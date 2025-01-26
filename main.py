import streamlit as st
from scrape import (
    scrape_website,
    split_don_content,
    clean_body_content,
    extract_body_content,
    extract_images  # Import the new function
)
from parse import parse_with_ollama

# Set page configuration
st.set_page_config(
    page_title="Scraper AI",
    page_icon="🌐",
    layout="wide"
)

# Custom CSS for professional styling
st.markdown(
    """
    <style>
    body {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(to bottom, #ff0000, #ffffff);
        color: #333;
    }
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #6a11cb, #2575fc);
        color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        font-size: 36px;
        margin-bottom: 10px;
    }
    .main-header p {
        font-size: 18px;
    }
    .content-box {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
    }
    .content-box h2 {
        font-size: 24px;
        margin-bottom: 10px;
        color: #333;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        font-size: 14px;
        color: #777;
    }
    .footer a {
        text-decoration: none;
        color: #6a11cb;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header with title and description
st.markdown(
    """
    <div class="main-header">
        <h1>Scraper AI</h1>
        <p>Extract and analyze website content effortlessly with AI-powered tools.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Input URL section
st.markdown("### 🔗 Enter Website URL")
url = st.text_input("Enter the website URL below:")

if st.button("Scrape Website"):
    st.info("Extracting website data... Please wait.")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)
    st.session_state.dom_content = cleaned_content
    st.session_state.html_content = result  # Store the raw HTML content for image extraction

    with st.expander("🔍 Extracted Content"):
        st.text_area("DOM Content", cleaned_content, height=300)

# Parsing section
if "dom_content" in st.session_state:
    st.markdown("### 🧠 Describe What You Want to Analyze")
    parse_description = st.text_area("Provide a description for analysis:")

    if st.button("Analyze Content"):
        st.info("Analyzing the content... Please wait.")
        dom_chunks = split_don_content(st.session_state.dom_content)
        result = parse_with_ollama(dom_chunks, parse_description)
        st.success("Content analysis complete!")
        st.markdown("### Analysis Results:")
        st.write(result)

# New button to extract and visualize all images
if "html_content" in st.session_state:
    if st.button("Extract and Display Images"):
        st.info("Extracting images... Please wait.")
        image_urls = extract_images(st.session_state.html_content, url)
        if image_urls:
            st.markdown("### 🖼️ Extracted Images:")
            for img_url in image_urls:
                st.image(img_url, caption="Image", width=300)  # Adjust width as needed
        else:
            st.warning("No images found in the HTML content.")

# Footer

