# 📊 ChatAnalyzer

ChatAnalyzer is a **Streamlit-powered** web application for analyzing chat conversations from **Telegram and WhatsApp**. It provides **insights, statistics, and visualizations** to understand user activity, word frequency, and message trends.

## 🚀 Features
✅ **Upload chat files** (`.json` for Telegram, `.txt` for WhatsApp).  
✅ **Automatic data cleaning** (removes service messages, normalizes timestamps & text).  
✅ **Chat statistics** (total messages, messages per user, common words).  
✅ **Visualizations** (messages over time, user activity).  
✅ **Fast processing** even for long conversations.  

---

## 👤 Project Structure

```
chatnalyzer/
│── data/                          # Ignored (local chat files)
│── src/                           # Source code
│   ├── data_loader.py             # Loads chat data from files
│   ├── data_cleaner.py            # Cleans and preprocesses messages
│   ├── eda.py                     # Generates chat insights and visualizations
│   ├── streamlit_app.py           # Streamlit web app
│── tests/                         # Test scripts
│   ├── test_data_loader.py
│   ├── test_data_cleaner.py
│   ├── test_eda.py
│── .env                           # Environment variables (ignored in Git)
│── .gitignore                     # Excludes sensitive files
│── requirements.txt               # Python dependencies
│── README.md                      # Project documentation
```

---

## 🛠 Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/YOUR-USERNAME/chatnalyzer.git
cd chatnalyzer
```

### **2️⃣ Create a Virtual Environment**
```bash
python -m venv venv
```

### **3️⃣ Activate the Virtual Environment**
- **Windows (PowerShell):**
  ```powershell
  venv\Scripts\Activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### **4️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Streamlit App
```bash
streamlit run src/streamlit_app.py
```
🔹 Open the app in your browser at `http://localhost:8501/`.

---

## 🧪 Running Tests
To verify that everything is working correctly, run:

```bash
python -m tests.test_data_loader
python -m tests.test_data_cleaner
python -m tests.test_eda
```

---

## 🔒 Privacy & Security
- **All uploaded chat data is processed locally** and **never sent to external servers**.
- Future versions will include **authentication and private cloud deployment options**.

---

## 🤝 Contributing
Contributions are welcome! To contribute:
1. **Fork the repo** and create a new branch.
2. Make your changes.
3. Submit a **Pull Request**.

---

## 🐟 License
This project is licensed under the **MIT License**.

---

## 🎯 Future Improvements
🔹 **WhatsApp support** (currently only Telegram JSON is fully supported).  
🔹 **Advanced filters** (filter messages by user, keyword, or time range).  
🔹 **Export reports** (CSV, PDF with chat insights).  
🔹 **Authentication & multi-user access** for private deployments.  

---

## 🌟 Contact
For questions or feature requests, feel free to reach out via **GitHub Issues**.

---

### **🚀 Ready to analyze your chats? Let's go!**

