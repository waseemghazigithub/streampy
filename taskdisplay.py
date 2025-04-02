import streamlit as st
import pandas as pd

def load_data(file):
    return pd.read_csv(file)

def main():
    st.title("Task Management Viewer")
    
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        st.write("### Task Data:")
        st.dataframe(df)
        
        # Allow users to download the data
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "task_data.csv", "text/csv")
    else:
        st.info("Please upload a CSV file to view the data.")

if __name__ == "__main__":
    main()
