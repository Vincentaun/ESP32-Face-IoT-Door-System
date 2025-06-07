

## IOT_Door

基於 ESP32 的人臉辨識智慧門禁系統

## **📖 專案簡介**

本專案旨在設計並實作一套以 ESP32-CAM 為核心的智慧門禁系統，結合人臉辨識技術、物聯網 (IoT) 與資料視覺化管理平台，達成自動化且安全的出入控制。

系統功能包含：

人臉影像即時辨識與本地端白名單比對。

LED 指示燈、蜂鳴器、伺服馬達之互動回饋。

資料庫紀錄訪問數據並透過網頁介面即時視覺化呈現。

## **⚙️ 系統架構**

系統分為四個模組進行整合：

影像辨識模組：ESP32-CAM，進行人臉影像擷取與即時辨識。

邏輯控制模組：負責系統內部控制邏輯與資料庫比對。

感測反饋模組：LED燈、蜂鳴器，提供視覺與聽覺即時回饋。

門禁驅動模組：SG90伺服馬達，模擬門鎖開關動作。

## **🚀 功能特色**

即時人臉辨識及授權管理。

網頁數據視覺化：登入紀錄、辨識準確率、時間分佈統計。

低成本、低功耗且高即時性。

模組化設計，易於擴充與維護。

## **🛠️ 技術棧**

硬體：ESP32-CAM、SG90 伺服馬達、LED、蜂鳴器

軟體：Python, Streamlit, OpenCV, MySQL, Arduino IDE

資料庫：MySQL

前端網頁視覺化框架：Streamlit, Altair

## **📊 網頁數據化管理平台**

本專案透過 Streamlit 建置視覺化管理平台，即時顯示以下數據：

使用者通知統計分析

使用時間區間分佈圖

最活躍使用者排行

即時人臉影像捕捉紀錄

## **🔐 資訊安全性**

使用 bcrypt 密碼雜湊提升帳戶安全性。

未來可整合雙重驗證（Two-Factor Authentication, 2FA）或生物識別技術。

## **📂 專案檔案結構**

ESP32-Face-IoT-Door-System/
├── Arduino/
│   └── face_recognition_control.ino
├── Web_Application/
│   ├── app.py
│   ├── requirements.txt
│   └── utils.py
├── Database/
│   └── iot_project.sql
└── README.md

## **⚡ 快速開始**

安裝 Python 環境與必要套件

pip install -r requirements.txt

匯入資料庫 (iot_project.sql)

mysql -u root -p < iot_project.sql

啟動網頁視覺化介面

streamlit run app.py

將 Arduino 程式上傳至 ESP32-CAM 並啟動設備

## **🎯 未來展望**

整合 Wi-Fi 遠端管理

加入 AI 深度學習人臉辨識技術

邊緣運算 (Edge Computing) 擴充

雲端數據分析與區塊鏈安全驗證

## **🏫 應用場域**

辦公室與企業內部安全管理

家庭住宅安全門禁

校園宿舍與實驗室安全管理

## **📝 聯絡作者**

如有任何疑問或建議，歡迎透過以下方式聯絡：

Email: Vincent: vincentaun123@gmail.com / LIN, YI-CHENG: 111B16885@mailst.cjcu.edu.tw

## **📄 授權條款**

本專案採用 MIT License 開源授權條款。
