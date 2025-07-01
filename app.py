#!/usr/bin/env python
# coding: utf-8

# # 📊 Where My Time Goes — A Personal Time Logger

# Track your daily activities and visualize where your time is actually going.
# 
# Built with Streamlit, Pandas, and a simple CSV file.
# 

# ### ✨ Features
# - Log daily activity (task + hours)
# - View full activity log
# - Weekly summary as a bar chart
# - Identify top time-consuming activity

# In[4]:


import pandas as pd
import streamlit as st
from datetime import datetime


# ## 🗂️ Load or Initialize Data
# 

# In[6]:


def load_data():
    try:
        return pd.read_csv("time_log.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Activity", "Hours"])


# ## 📝 Save Activity to File
# 

# In[8]:


def save_activity(date, activity, hours):
    df = load_data()
    new_row = pd.DataFrame([[date, activity, hours]], columns=["Date", "Activity", "Hours"])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("time_log.csv", index=False)


# ## 🖼️ Streamlit App UI
# 

# In[10]:


st.set_page_config(page_title="Where My Time Goes", layout="centered")
st.title("📊 Where My Time Goes")
st.caption("Track your daily time logs and get a weekly insight into your activity pattern.")


# ## 📥 User Input Form

# In[12]:


with st.form("log_form"):
    date = st.date_input("Date", datetime.today())
    activity = st.text_input("Activity (e.g., Study, Sleep, Scroll)")
    hours = st.number_input("Hours Spent", min_value=0.0, max_value=24.0, step=0.5)
    submitted = st.form_submit_button("Log Time")

    if submitted:
        if activity and hours > 0:
            save_activity(date, activity, hours)
            st.success("✅ Activity logged!")
        else:
            st.error("❗ Please enter both activity and hours.")


# ## 📋 View Activity Log

# In[14]:


df = load_data()

if not df.empty:
    st.subheader("📋 Activity Log")
    st.dataframe(df)

    df["Date"] = pd.to_datetime(df["Date"])
    recent = df[df["Date"] >= (datetime.today() - pd.Timedelta(days=7))]


# ## 📈 Weekly Summary Chart

# In[16]:


if not df.empty:
    st.subheader("📋 Activity Log")
    st.dataframe(df)

    df["Date"] = pd.to_datetime(df["Date"])
    recent = df[df["Date"] >= (datetime.today() - pd.Timedelta(days=7))]

    if not recent.empty:
        st.subheader("📈 Time Spent This Week")
        summary = recent.groupby("Activity")["Hours"].sum().sort_values(ascending=False)
        st.bar_chart(summary)
        st.markdown(f"**Top activity:** `{summary.idxmax()}` – `{summary.max()} hrs`")
    else:
        st.info("No activity logged in the last 7 days.")
else:
    st.info("Start by logging your first activity above ☝️")


# ## 🔚 Footer

# In[18]:


st.markdown("---")
st.caption("Made with Streamlit + ☕ by [Nandini Vyas](https://www.linkedin.com/in/nandini-vyas-27b142368)")


# In[ ]:




