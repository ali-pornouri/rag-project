<div align="center">

# 🤖 RAG System — Intelligent Question Answering
# سیستم پرسش و پاسخ هوشمند

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-latest-green)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA3.3-orange)](https://groq.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-latest-purple)](https://chromadb.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-latest-red)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

</div>

---

## 🇬🇧 English

### 📌 Description
A powerful **RAG (Retrieval Augmented Generation)** system that lets you 
chat intelligently with your own documents. Upload any PDF or TXT file 
and get accurate answers with exact source references (book name + page number).

### ✨ Features
- 📄 Upload multiple PDF and TXT files simultaneously
- 🔍 Semantic Search across all documents
- 🤖 Intelligent answers powered by Groq (LLaMA 3.3)
- 📚 Source citation — exact book name and page number
- 🔑 Hash-based duplicate detection — prevents duplicate indexing
- 🗑️ Delete specific documents from the database
- 📊 Real-time progress bar during indexing
- 💬 Bilingual interface — Persian & English
- 💾 Persistent vector database — data survives restarts
- 🎨 Modern dark UI with RTL support for Persian

### 🛠️ Tech Stack
| Tool | Purpose |
|------|---------|
| Python 3.13 | Core language |
| LangChain | RAG framework |
| ChromaDB | Persistent vector database |
| Sentence Transformers | Embedding model (all-MiniLM-L6-v2) |
| Groq (LLaMA 3.3) | Language model |
| Streamlit | Web interface |
| python-dotenv | Secure API key management |

### 🚀 Getting Started

#### 1. Clone the repository
```bash
git clone https://github.com/ali-pornouri/rag-project.git
cd rag-project
```

#### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set up environment variables
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_token_here
```
Get your free Groq API key at: https://console.groq.com

#### 5. Run the application
```bash
streamlit run app.py
```

#### 6. Use the system
1. Upload your PDF or TXT files
2. Click "Index Documents"
3. Wait for the progress bar to complete
4. Ask any question in the chat
5. Get accurate answers with source references!

### 📁 Project Structure
```
rag-project/
├── app.py              # Streamlit web interface
├── config.py           # Project configuration & settings
├── ingest.py           # Document loading, indexing & management
├── rag.py              # Question answering system
├── requirements.txt    # Python dependencies
├── .env                # API keys (not in Git)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### ⚙️ Configuration
All settings are in `config.py`:
```python
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Embedding model
CHUNK_SIZE = 300                        # Text chunk size
CHUNK_OVERLAP = 50                      # Chunk overlap
GROQ_MODEL = "llama-3.3-70b-versatile" # LLM model
MAX_TOKENS = 600                        # Max response tokens
TEMPERATURE = 0.2                       # Response creativity
TOP_K = 3                               # Retrieved chunks count
```
---

## 🇮🇷 فارسی

### 📌 توضیحات
یک سیستم قدرتمند **RAG** که به شما امکان می‌دهد با اسناد خودتان 
به صورت هوشمند گفتگو کنید. هر فایل PDF یا TXT آپلود کنید و 
جواب دقیق با ذکر منبع (نام کتاب + شماره صفحه) دریافت کنید.

### ✨ قابلیت‌ها
- 📄 آپلود چندین فایل PDF و TXT به طور همزمان
- 🔍 جستجوی معنایی در تمام اسناد
- 🤖 پاسخ هوشمند با Groq (LLaMA 3.3)
- 📚 ذکر منبع دقیق — نام کتاب و شماره صفحه
- 🔑 تشخیص تکراری با Hash — جلوگیری از ایندکس مضاعف
- 🗑️ حذف اسناد خاص از پایگاه داده
- 📊 نوار پیشرفت در زمان واقعی
- 💬 رابط دو زبانه — فارسی و انگلیسی
- 💾 پایگاه داده ماندگار — داده‌ها بعد از ری‌استارت حفظ میشن
- 🎨 رابط کاربری تاریک مدرن با پشتیبانی RTL فارسی

### 🚀 نصب و راه‌اندازی

#### ۱. کلون کردن پروژه
```bash
git clone https://github.com/ali-pornouri/rag-project.git
cd rag-project
```

#### ۲. ساخت محیط مجازی
```bash
python -m venv venv
venv\Scripts\activate
```

#### ۳. نصب کتابخانه‌ها
```bash
pip install -r requirements.txt
```

#### ۴. تنظیم توکن Groq
فایل `.env` بساز:
```
GROQ_API_KEY=توکن_گروک_شما
```
توکن رایگان از: https://console.groq.com

#### ۵. اجرای برنامه
```bash
streamlit run app.py
```

#### ۶. نحوه استفاده
1. فایل PDF یا TXT آپلود کن
2. روی "ایندکس کردن اسناد" کلیک کن
3. صبر کن تا progress bar تموم بشه
4. هر سوالی بپرس
5. جواب دقیق + منبع دریافت کن!

### 📁 ساختار پروژه
```
rag-project/
├── app.py              # رابط کاربری Streamlit
├── config.py           # تنظیمات پروژه
├── ingest.py           # بارگذاری، ایندکس و مدیریت اسناد
├── rag.py              # سیستم پرسش و پاسخ
├── requirements.txt    # کتابخانه‌های Python
├── .env                # توکن API (در Git نیست)
├── .gitignore          # قوانین نادیده گرفتن Git
└── README.md           # این فایل
```

---

## 📁 Project Structure / ساختار پروژه
```
rag-project/
├── app.py              # رابط کاربری / Web interface
├── config.py           # تنظیمات / Configuration
├── ingest.py           # ایندکس / Document indexing
├── rag.py              # پرسش و پاسخ / Q&A system
├── requirements.txt    # کتابخانه‌ها / Dependencies
├── .env                # توکن / API keys (not in Git)
├── .gitignore          # Git ignore
└── README.md           # مستندات / Documentation
```

---

<div align="center">

## 👨‍💻 Developer / توسعه‌دهنده

**Ali Pornouri** — [@ali-pornouri](https://github.com/ali-pornouri)

---

🇮🇷 Made with ❤️ in Italy 🇮🇹

⭐ If you find this useful, please give it a star!
⭐ اگه مفید بود، ستاره بده!

</div>
```
## 🤝 Contributing / مشارکت

Contributions are welcome! If you find this project useful:
- ⭐ Give it a star
- 🍴 Fork it and improve it
- 🐛 Report bugs via Issues
- 💡 Suggest features via Issues

اگه این پروژه مفید بود:
- ⭐ ستاره بده
- 🍴 Fork کن و بهترش کن
- 🐛 باگ‌ها رو توی Issues گزارش بده