import streamlit as st
import pandas as pd
import altair as alt
import datetime
from PIL import Image
import io
from utils import (
    get_connection, register_user, authenticate_user, decode_image
)

def main():
    st.set_page_config(page_title="IoT Project Dashboard | Real-time Access Control", layout="wide")
    st.sidebar.title("🔐 Authentication & Filters")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''

    menu = ["Dashboard", "Logout"] if st.session_state['logged_in'] else ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Register":
        st.title("🆕 Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        new_password_confirm = st.text_input("Confirm Password", type='password')
        if st.button("Register"):
            if new_password != new_password_confirm:
                st.error("Passwords do not match")
            else:
                success, msg = register_user(new_user, new_password)
                st.success(msg) if success else st.error(msg)

    elif choice == "Login":
        st.title("🔑 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success(f"Welcome, **{username}**!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    elif choice == "Logout":
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''
        st.success("Logged out successfully.")
        st.rerun()

    elif choice == "Dashboard":
        st.title(f"📡 IoT Access Control Dashboard - Welcome, {st.session_state['username']}")

        conn = get_connection()
        df_noti = pd.read_sql("SELECT * FROM noti", conn)
        df_noti['timestamp'] = pd.to_datetime(df_noti['timestamp'])
        conn.close()

        st.sidebar.header("📅 Data Filters")
        start_date = st.sidebar.date_input("Start date", datetime.date.today() - datetime.timedelta(days=7))
        end_date = st.sidebar.date_input("End date", datetime.date.today())

        mask = (df_noti['timestamp'].dt.date >= start_date) & (df_noti['timestamp'].dt.date <= end_date)
        filtered_noti = df_noti.loc[mask]

        st.info(f"Showing data from **{start_date}** to **{end_date}**")

        st.subheader("👤 User Notification Activity")
        user_counts = filtered_noti['username'].value_counts().reset_index(name='count')
        chart_user = alt.Chart(user_counts).mark_bar(size=40).encode(
            x='index:N',
            y='count:Q',
            tooltip=['index', 'count']
        ).properties(width=600)
        st.altair_chart(chart_user, use_container_width=True)

        st.subheader("⏰ Notification Time Distribution")
        time_counts = filtered_noti['time_period'].value_counts().reset_index(name='count')
        chart_time = alt.Chart(time_counts).mark_arc(innerRadius=70).encode(
            theta='count',
            color='time_period',
            tooltip=['time_period', 'count']
        ).properties(width=400)
        st.altair_chart(chart_time, use_container_width=True)

        st.subheader("🏅 Top 5 Active Users")
        top_users = user_counts.head(5)
        st.table(top_users)

        st.subheader("📸 Latest Captured Images")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, picture FROM pictures ORDER BY timestamp DESC LIMIT 9")
        images_db = cursor.fetchall()
        conn.close()

        if images_db:
            cols = st.columns(3)
            for idx, (timestamp, blob_data) in enumerate(images_db):
                try:
                    img_data = decode_image(blob_data)
                    img = Image.open(io.BytesIO(img_data))
                    cols[idx % 3].image(img, caption=f"{timestamp}", use_column_width=True)
                except Exception as e:
                    st.warning(f"⚠️ Error loading image: {e}")
        else:
            st.info("No images to display.")

if __name__ == "__main__":
    main()
