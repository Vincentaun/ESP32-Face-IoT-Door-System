# 🧠 基於 ESP32 的人臉辨識智慧門禁系統

> 使用 ESP32-CAM、Streamlit 與 MySQL 建構的物聯網門禁系統，結合人臉辨識與數據視覺化面板。

---

## 📘 專案簡介

本專案旨在設計並實作一套以 **ESP32-CAM** 為核心的智慧門禁系統，結合人臉辨識技術、物聯網（IoT）與資料視覺化管理平台，達成自動化且安全的出入控制。

### 🎯 系統功能包含：
- ✅ 即時人臉影像辨識與白名單比對  
- ✅ LED、蜂鳴器、伺服馬達回饋控制  
- ✅ MySQL 資料庫紀錄存取紀錄  
- ✅ 網頁端視覺化呈現與登入系統  

---

## 🧱 系統架構模組

- 📷 **影像辨識模組**：ESP32-CAM 擷取與辨識臉部影像  
- 🧠 **邏輯控制模組**：ESP32 程式進行資料比對與判斷邏輯  
- 💡 **感測反饋模組**：LED、蜂鳴器提供提示回饋  
- 🔒 **門禁驅動模組**：SG90 伺服馬達模擬門鎖動作  

---

## ✨ 特色功能

- 📡 即時人臉辨識與授權管理  
- 📊 Streamlit 數據視覺化儀表板  
- 🔐 使用者登入系統與密碼雜湊（bcrypt）  
- ⚙️ 模組化程式架構，方便擴充與維護  
- 🌐 適合多種場域（家用、校園、企業）  

---

## 🧰 技術棧

| 類別     | 技術內容                           |
|----------|------------------------------------|
| 硬體     | ESP32-CAM, SG90, LED, 蜂鳴器       |
| 軟體     | Python, Streamlit, OpenCV, Arduino |
| 資料庫   | MySQL                              |
| 前端框架 | Streamlit, Altair                  |

---

## 🖥️ 數據視覺化功能（Web 平台）

- 👤 使用者通知統計圖（Bar Chart）  
- 🕐 時段分佈甜甜圈圖（Donut Chart）  
- 🏆 活躍使用者排行榜  
- 📸 入侵者即時影像截圖展示  

---

## **🔐 資訊安全性**

- 使用 bcrypt 密碼雜湊提升帳戶安全性。

- 未來可整合雙重驗證（Two-Factor Authentication, 2FA）或生物識別技術。

## **📂 專案檔案結構**
```
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
```

## **⚡ 快速開始**

安裝 Python 環境與必要套件
```
pip install -r requirements.txt
```

匯入資料庫 (iot_project.sql)
```
mysql -u root -p < iot_project.sql
```

啟動網頁視覺化介面
```
streamlit run app.py
```

將 Arduino 程式上傳至 ESP32-CAM 並啟動設備

## **🎯 未來展望**

- ☁️ 整合 Wi-Fi 遠端管理與通知

- 🤖 導入深度學習式人臉辨識

- 🧠 擴展邊緣運算能力（Edge AI）

- 🔗 將數據串接雲端與區塊鏈驗證

## **🏫 應用場域**

- 🏠 家庭住宅門禁

- 🏫 校園宿舍與實驗室

- 🏢 辦公室內部控管

## **📝 聯絡作者**

如有任何疑問或建議，歡迎透過以下方式聯絡：<br/>
Email: Vincent: vincentaun123@gmail.com / 111B16885@mailst.cjcu.edu.tw <br/>
&emsp;&emsp;&emsp;LIN, YI-CHENG: 111B15219@mailst.cjcu.edu.tw
## **📄 授權條款**

本專案採用 MIT License 開源授權條款。
