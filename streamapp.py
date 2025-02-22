import streamlit as st
import pandas as pd
import os 
from io import BytesIO
import openpyxl

# Set up the app
st.set_page_config(page_title="📀 Data Sweeper", layout='wide')

st.title("📀 Data Graph")
st.write("Upload data file with user picture and view your graph!")

# Sidebar for camera input
st.sidebar.subheader("📸 Active User")
image = st.sidebar.camera_input("Take a picture")

if image:
    st.sidebar.image(image)

# Sidebar for social media selection
st.sidebar.subheader("🌐 Select Social Media Platform")
social_media = st.sidebar.selectbox("Choose a platform", ["Select", "YouTube", "Facebook", "LinkedIn", "Twitter", "Others"])

# Social media URLs
social_media_urls = {
    "YouTube": "https://www.youtube.com",
    "Facebook": "https://www.facebook.com",
    "LinkedIn": "https://www.linkedin.com",
    "Twitter": "https://www.twitter.com",
    "Others": "https://www.google.com"
}


upload_file = st.file_uploader("Upload a file (CSV or Excel)", type=['csv', 'xlsx', 'xls'], accept_multiple_files=True)

# Main content
if upload_file:
    for file in upload_file:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext in [".xlsx", ".xls"]:
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format: {file_ext}")
            continue

        # Display file info
        st.write("🔎 Preview the head of the DataFrame")
        st.dataframe(df.head())

        st.subheader("🔄 Graph Conversion ")
        conversion_type = st.radio(f"Select Graph type", ["Bar", "Line","Area"], key=file.name)

        if conversion_type == "Bar":
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
        elif conversion_type == "Line":
            st.line_chart(df.select_dtypes(include='number').iloc[:,:2])
        elif conversion_type == "Area":
            st.area_chart(df.select_dtypes(include='number').iloc[:,:2])
        st.success("🎉 All files processed!")
