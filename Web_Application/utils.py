import pymysql
import bcrypt
import base64
import urllib.parse

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Vincentaun-1128',
        db='iot_project',
        charset='utf8mb4'
    )

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
        return bcrypt.checkpw(password.encode(), stored_hash)
    return False

def fix_base64_padding(data):
    data = data.strip().replace('\n', '').replace('\r', '')
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    return data

def decode_image(blob_data):
    base64_str = blob_data.decode('utf-8')
    if base64_str.startswith('data:image'):
        base64_data = base64_str.split(',')[1]
    else:
        base64_data = base64_str
    base64_data = urllib.parse.unquote(base64_data)
    safe_base64_data = fix_base64_padding(base64_data)
    return base64.b64decode(safe_base64_data)
