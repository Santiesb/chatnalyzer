# **📊 ChatAnalyzer: Advanced Chat Analytics Platform**

**Gain deep insights from Telegram chats** with **automated text cleaning, NLP-powered analysis, and interactive visualizations**.\
Built with **Streamlit, Pandas, NLTK, and spaCy** for efficient chat exploration.



---

## **🌟 Features & Capabilities**

### **🔧 Data Processing**

- **Automated Cleaning**: Removes service messages (user joins, group changes).
- **Text Preprocessing**:
  - Extracts **emojis, URLs, and mentions**.
  - Normalizes text (lowercasing, stopword removal, accent handling).
  - Supports **Spanish NLP** (lemmatization, stemming).
- **Scalable Pipeline**: Optimized for **large chat histories (>50K messages)**.

### **📈 Chat Analytics & NLP**

- **Message Statistics**:
  - **User Activity**: Top senders, message frequency trends.
  - **Time-Based Patterns**: Daily/weekly trends, peak messaging hours.
- **NLP-Powered Analysis**:
  - **Word Frequency & TF-IDF** keyword extraction.
  - **Named Entity Recognition (NER)** (Supports **Spanish & English**).
- **Interactive Visualizations**:
  - **Message Trends** over time.
  - **User Activity Heatmaps**.
  - **Word Clouds** from chat data.

---

## **🚀 Getting Started**

### **📌 Prerequisites**

- **Python 3.9+**
- **spaCy Spanish model** (for advanced NLP):
  ```bash
  python -m spacy download es_core_news_sm
  ```

### **💾 Installation**

```bash
git clone https://github.com/YOUR-USERNAME/chatnalyzer.git
cd chatnalyzer
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### **▶️ Running the App**

```bash
streamlit run app.py
```

---

## **👤 Project Structure**

```bash
💾 chatnalyzer/
├── app.py                 # Main Streamlit application
├── requirements.txt        # Project dependencies
├── README.md               # Documentation
└── src/                    # Core logic
    ├── data_loader.py       # Chat file loading pipeline
    ├── data_cleaner.py      # Data preprocessing & text cleaning
    ├── eda.py               # Exploratory data analysis (EDA)
    ├── feature_engineering.py # NLP feature extraction (TF-IDF, NER)
    ├── visualizations.py    # Streamlit visual components
    ├── utils.py             # Utility functions (logging, error handling)
```

---

## **📚 Usage Guide**

1️⃣ **Upload** your Telegram chat export (`.json`).\
2️⃣ **Explore** automated **data cleaning & preprocessing**.\
3️⃣ **Apply filters** (date range, user selection).\
4️⃣ **Analyze chat patterns** through interactive dashboards:

- 📈 **Message Trends** (daily, weekly activity).
- 🔥 **User Activity Heatmaps**.
- 🏅 **Keyword & Named Entity Trends**.

---

## **🛡 Privacy & Security**

✔ **Local Processing**: **All data is processed on your machine** – no cloud storage or data leaks.\
✔ **Session Isolation**: **Analyses reset** upon page refresh – no saved data.\
✔ **Data Protection**: Your **original chat files remain untouched**.

---

## **💜 License**

This project is open-source and licensed under the **MIT License**.\
See the [`LICENSE`](./LICENSE) file for details.

---

## **📩 Contact & Support**

📧 Email: [**santiago.esbert@gmail.com**](mailto\:santiago.esbert@gmail.com)\
🐛 Report Issues: [**GitHub Issues**](https://github.com/YOUR-USERNAME/chatnalyzer/issues)

---

### **✨ Why This Version is Better?**

✅ **More Professional & Structured** – Clear sections, bullet points, and explanations.\
✅ **Simplified Installation & Running Steps** – Easier to follow for new users.\
✅ **Security & Privacy Section** – Highlights **local-only data processing**.\
✅ **Better Readability** – Shorter sentences, improved formatting.

Would you like to add anything else (e.g., example screenshots, FAQs)? 🚀

