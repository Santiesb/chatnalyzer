# 📊 ChatAnalyzer: Advanced Chat Analytics Platform

**Uncover insights from Telegram chats** with automated cleaning, NLP-powered analysis, and interactive visualizations. Built with Streamlit, spaCy, and NLTK.

![Chat Analytics Dashboard](https://via.placeholder.com/800x400.png?text=Chat+Analytics+Dashboard+Preview)

## 🌟 Key Features

### 🔧 Data Processing
- **Smart Cleaning**: Auto-removes service messages, normalizes timestamps
- **Text Processing**:
  - Emoji/URL extraction
  - Accent normalization & stopword removal
  - Spanish text support (lemmatization/stemming)
- **Efficient Pipelines**: Handles large chat histories (>50k messages)

### 📈 Analytics & NLP
- **Message Statistics**: 
  - User activity trends
  - Hourly/daily/weekly patterns
- **NLP Features**:
  - Word frequency analysis
  - TF-IDF keyword extraction
  - Named Entity Recognition (Spanish/English)
- **Interactive Visuals**:
  - Message time series
  - Activity heatmaps
  - Word clouds

### 🛠 Tech Stack
- **Backend**: Python 3.9+, Pandas, NLTK, spaCy
- **Visualization**: Streamlit, Altair, Matplotlib
- **NLP**: SnowballStemmer, WordNetLemmatizer

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- spaCy Spanish model:
  ```bash
  python -m spacy download es_core_news_sm

### 🌟 Installation

git clone https://github.com/YOUR-USERNAME/chatnalyzer.git
cd chatnalyzer
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

### Launch app
streamlit run app.py

### 📂 Project Structure
.
├── app.py                 # Main Streamlit application
├── src/
│   ├── data_loader.py          # Data loading pipleine
│   ├── data_cleaner.py         # Message cleaning pipeline
│   ├── eda.py                  # Exploratory data analysis
│   ├── feature_engineering.py  # NLP feature extraction
│   └── visuals.py              # Visualization components
├── requirements.txt            # Dependency list
└── README.md                   # This documentation


## 🔍 Usage Guide
1. Upload your Telegram chat export (.json)

2. Explore automated data cleaning steps

3. Filter by date range or specific users

4. Analyze through interactive tabs:
  - Temporal message patterns
  - User activity comparisons
  - Keyword/Named Entity trends

## 🛡 Privacy & Security
Local Processing: No data leaves your machine

Session Isolation: Analyses reset on page reload

Clean Data Handling: Original chats never stored

## 📜 License
MIT License - See LICENSE for details

## 📬 Contact
For feature requests or issues:
📧 santiago.esbert@gmail.com
🐛 GitHub Issues