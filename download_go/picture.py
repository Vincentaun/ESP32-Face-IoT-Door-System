import pymysql
import time
import os

output_folder = r"C:\Users\User\Desktop\PHP\saved_images\\"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

seen_timestamps = set()

while True:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='Vincentaun-1128',
        db='iot_project',
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, picture FROM pictures")
    results = cursor.fetchall()

    for timestamp, blob in results:
        if timestamp not in seen_timestamps:
            filename = f"{output_folder}image_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'wb') as f:
                f.write(blob)
            print(f"Saved {filename}")
            seen_timestamps.add(timestamp)

    conn.close()
    time.sleep(10)  # Wait 10 seconds before next check
