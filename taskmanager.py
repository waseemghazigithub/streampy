import streamlit as st
import pandas as pd
import os


# File to store tasks
data_file = "tasks.csv"

def load_tasks():
    if os.path.exists(data_file):
        return pd.read_csv(data_file)
    return pd.DataFrame(columns=["Description", "Status", "Expected Date", "Person Engaged"])

def save_tasks(df):
    df.to_csv(data_file, index=False)

def main():
    st.title("📅 Project Task Schedule Manager")
    df = load_tasks()
    
    menu = ["Add Task", "Remove Task", "Search Task", "Display All Tasks", "Task Statistics"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Add Task":
        st.subheader("➕ Add a New Task")
        desc = st.text_input("Task Description")
        status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
        date = st.date_input("Expected Date")
        person = st.text_input("Person Engaged")
        
        if st.button("Add Task"):
            new_task = pd.DataFrame([{"Description": desc, "Status": status, "Expected Date": date, "Person Engaged": person}])
            df = pd.concat([df, new_task], ignore_index=True)
            save_tasks(df)
            st.success("Task added successfully!")
    
    elif choice == "Remove Task":
        st.subheader("🗑️ Remove a Task")
        task_to_remove = st.text_input("Enter Task Description to Remove")
        
        if st.button("Remove Task"):
            df = df[df["Description"] != task_to_remove]
            save_tasks(df)
            st.success("Task removed successfully!")
    
    elif choice == "Search Task":
        st.subheader("🔍 Search for a Task")
        search_query = st.text_input("Enter Task Description to Search")
        
        if st.button("Search"):
            results = df[df["Description"].str.contains(search_query, case=False, na=False)]
            st.write(results if not results.empty else "No tasks found.")
    
    elif choice == "Display All Tasks":
        st.subheader("📋 All Tasks")
        st.dataframe(df)
    
    elif choice == "Task Statistics":
        st.subheader("📊 Task Statistics")
        st.write("Total Tasks:", len(df))
        st.write(df["Status"].value_counts())
    
if __name__ == "__main__":
    main()
