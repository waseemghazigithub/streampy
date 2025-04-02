import streamlit as st
import pandas as pd

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;  # Adjust the value as needed (0rem to remove)
    }
    </style>
    """,
    unsafe_allow_html=True
)

#st.title("Maxim Group of Companies")

def load_data():
    # Use the fixed CSV file path here
    file_path = 'tasks.csv'  # Ensure this is the correct path to your CSV file
    return pd.read_csv(file_path)

def main():
    st.subheader("Maxim Group of Companies Software Upgradation")
    st.markdown('<u>**1. Green Field City Data Migration/rquired frontend forms/reports**</u>', unsafe_allow_html=True)
    st.text("Objective: Data migration Ms.Access to Sql Server and development of required forms/reports. Completion Target Date: April 5, 2025")
    st.markdown('<u>**2. MDA Recovery Software**</u>', unsafe_allow_html=True)
    st.text("Objective: Complete data migration FoxPro for Dos to Sql Server, development of required forms/reports, and output documentation. Completion Target Date: September 2026 (including testing and parallel running)")
    st.markdown('<u>**3. Accounting Financial Module**</u>', unsafe_allow_html=True) 
    st.text("Objective: Development a complete financial module with integration of Maxim Agro Activity Module.")
    # Load the fixed CSV data directly
    df = load_data()
    #st.dataframe(df)
    menu = ["All Projects","Green Field City", "M.D.A", "Accounting Financial Module", "Task Statistics"]
    choice = st.sidebar.selectbox("Projects", menu)
    
    if choice == "All Projects":
        st.subheader(f"Task Breakdown: {choice}")
        st.dataframe(df)

    if choice == "Green Field City":
         st.subheader(f"Task Breakdown: {choice}")
         green_field_df = df[df['Project'] == 'Green Field City']
         st.dataframe(green_field_df)
    if choice == "M.D.A":
         st.subheader(f"Task Breakdown: {choice}")
         green_field_df = df[df['Project'] == 'M.D.A']
         st.dataframe(green_field_df) 
    if choice == "Accounting Financial Module":
        st.subheader(f"Task Breakdown: {choice}")
        green_field_df = df[df['Project'] == 'Accounting Financial Module']
        st.dataframe(green_field_df)
    if choice == "Task Statisticse":
        st.subheader(f"Task Breakdown: {choice}")

    # # Allow users to download the fixed data
    # csv = df.to_csv(index=False).encode('utf-8')
    # st.download_button("Download CSV", csv, "task_data.csv", "text/csv")

if __name__ == "__main__":
    main()
