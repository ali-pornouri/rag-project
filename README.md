# 🤖 RAG System — سیستم پرسش و پاسخ هوشمند

یک سیستم RAG (Retrieval Augmented Generation) که با استفاده از 
LangChain، ChromaDB و Groq ساخته شده است.

## ✨ قابلیت‌ها
- بارگذاری فایل‌های PDF و TXT
- جستجوی معنایی (Semantic Search)
- پاسخ هوشمند با Groq LLM
- پشتیبانی از چند فایل همزمان

## 🛠️ تکنولوژی‌ها
- Python 3.13
- LangChain
- ChromaDB
- Sentence Transformers
- Groq (LLaMA 3.3)

## 🚀 نصب و راه‌اندازی

### ۱. کلون کردن پروژه
```bash
git clone https://github.com/Ali8498/rag-project.git
cd rag-project
```

### ۲. ساخت محیط مجازی
```bash
python -m venv venv
venv\Scripts\activate
```

### ۳. نصب کتابخانه‌ها
```bash
pip install -r requirements.txt
```

### ۴. تنظیم توکن Groq
فایل `.env` بساز و توکن Groq رو اضافه کن:
```
GROQ_API_KEY=your_token_here
```

### ۵. ایندکس کردن اسناد
```bash
python ingest.py
```

### ۶. پرسش و پاسخ
```bash
python rag.py
```

## 📁 ساختار پروژه
```
rag-project/
├── config.py          # تنظیمات پروژه
├── ingest.py          # بارگذاری و ایندکس اسناد
├── rag.py             # سیستم پرسش و پاسخ
├── requirements.txt   # کتابخانه‌ها
└── .gitignore         # فایل‌های نادیده
```

## 👨‍💻 توسعه‌دهنده
Ali Pornouri — [@Ali8498](https://github.com/Ali8498)
```

---

**Ctrl+S** بزن و بعد این دستورات رو بزن:
```
git add README.md
git commit -m "docs: add professional README"
git push