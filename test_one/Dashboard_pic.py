import streamlit as st
import pandas as pd
import pymysql
import os
import base64
import urllib.parse
import io
import datetime
from PIL import Image
import altair as alt
import bcrypt

# === Database connection helper ===
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='SQLpassword',
        db='iot_project',
        charset='utf8mb4'
    )

# === User auth functions ===
def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "Username already exists."
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, pw_hash.decode()))
    conn.commit()
    conn.close()
    return True, "User registered successfully."

def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        stored_hash = result[0].encode()
        if bcrypt.checkpw(password.encode(), stored_hash):
            return True
    return False

# === Base64 padding fixer ===
def fix_base64_padding(data):
    data = data.strip().replace('\n', '').replace('\r', '')
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    return data



# === Main app ===
def main():
    st.set_page_config(page_title="IoT Project Dashboard with Auth", layout="wide")
    st.sidebar.title("🔐 User Authentication & Filters")

    # Session state initialization
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''

    # Auth menu
    if st.session_state['logged_in']:
        menu = ["Dashboard", "Logout"]
    else:
        menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    # --- REGISTER ---
    if choice == "Register":
        st.title("Create New Account")
        new_user = st.text_input("Username", key="reg_user")
        new_password = st.text_input("Password", type='password', key="reg_pass")
        new_password_confirm = st.text_input("Confirm Password", type='password', key="reg_pass_conf")
        if st.button("Register"):
            if not new_user or not new_password:
                st.warning("Please fill all fields")
            elif new_password != new_password_confirm:
                st.error("Passwords do not match")
            else:
                success, msg = register_user(new_user, new_password)
                if success:
                    st.success(msg)
                    st.info("Go to Login menu to log in.")
                else:
                    st.error(msg)

    # --- LOGIN ---
    elif choice == "Login":
        st.title("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type='password', key="login_pass")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success(f"Welcome {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    # --- LOGOUT ---
    elif choice == "Logout":
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''
        st.success("You have been logged out.")
        st.rerun()

    # --- DASHBOARD ---
    elif choice == "Dashboard":
        
        def get_images_from_db():
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, picture FROM pictures")  # Modify query as needed
            results = cursor.fetchall()
            conn.close()
            return results
        
        
        st.title(f"🚀 IoT Project Dashboard — Welcome {st.session_state['username']}")

        # Load and filter data
        conn = get_connection()
        df_noti = pd.read_sql("SELECT * FROM noti", conn)
        conn.close()
        df_noti['timestamp'] = pd.to_datetime(df_noti['timestamp'])

        # Sidebar filters for dashboard
        st.sidebar.header("📅 Data Filters")
        start_date = st.sidebar.date_input("Start date", value=datetime.date.today() - datetime.timedelta(days=7))
        end_date = st.sidebar.date_input("End date", value=datetime.date.today())
        mask = (df_noti['timestamp'].dt.date >= start_date) & (df_noti['timestamp'].dt.date <= end_date)
        filtered_noti = df_noti.loc[mask]

        st.write(f"Showing data from **{start_date}** to **{end_date}**")

        # Notification counts per user
        st.subheader("🔔 Notification Counts per User")
        user_counts = filtered_noti.groupby('username').size().reset_index(name='count')
        chart_user = alt.Chart(user_counts).mark_bar(color='#4C78A8').encode(
            x=alt.X('username:N', title='Username'),
            y=alt.Y('count:Q', title='Notification Count'),
            tooltip=['username', 'count']
        ).properties(width=600, height=300)
        st.altair_chart(chart_user, use_container_width=True)

        # Notification distribution by time period
        st.subheader("⏰ Notification Distribution by Time Period")
        time_counts = filtered_noti['time_period'].value_counts().reset_index()
        time_counts.columns = ['time_period', 'count']
        chart_time = alt.Chart(time_counts).mark_arc().encode(
            theta=alt.Theta(field="count", type="quantitative"),
            color=alt.Color(field="time_period", type="nominal"),
            tooltip=['time_period', 'count']
        ).properties(width=400, height=400)
        st.altair_chart(chart_time, use_container_width=True)

        # Top 5 active users
        st.subheader("🏆 Top 5 Most Active Users")
        top_users = (
            filtered_noti.groupby('username')
            .size()
            .reset_index(name='count')
            .sort_values('count', ascending=False)
            .head(5)
        )
        st.table(top_users)

        # Show images
        st.subheader("📸 Latest Captured Pictures")
        
        images_db = get_images_from_db() 
        # folder_path = r"C:\Users\User\Desktop\PHP\saved_images\\"
        # image_output_folder = r"C:\Users\User\Desktop\PHP\saved_images\jpg_output\\"

        images = []
        for item in images_db:
            if item[1]:
                base64_str = item[1].decode('utf-8')  # Assuming the image is stored as a BLOB in the database
                if base64_str.startswith('data:image'):
                    base64_data = base64_str.split(',')[1]
                else:
                    base64_data = base64_str

                base64_data = urllib.parse.unquote(base64_data)
                safe_base64_data = fix_base64_padding(base64_data)

                try:
                    image_bytes = base64.b64decode(safe_base64_data)
                    image = Image.open(io.BytesIO(image_bytes))
                    images.append(image)

                except Exception as e:
                    st.warning(f"⚠️ Failed to decode image {item}: {e}")

        if images:
            cols = st.columns(3)
            for idx, img in enumerate(images[:9]):
                with cols[idx % 3]:
                    st.image(img, use_container_width=True, caption=f"Image {idx + 1}")
        else:
            st.info("No images found to display.")

        # Clickable links for saved images
        # st.subheader("🔗 Clickable Saved Image Files")
        # if os.path.exists(image_output_folder):
        #     jpg_files = sorted([f for f in os.listdir(image_output_folder) if f.endswith('.jpg')])
        #     for img_file in jpg_files:
        #         file_path = os.path.join(image_output_folder, img_file)
        #         st.markdown(f"[📷 {img_file}](file:///{file_path})")
        # else:
        #     st.info("No saved .jpg image files found.")

if __name__ == "__main__":
    main()
