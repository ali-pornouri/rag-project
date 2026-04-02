# Base image — Python 3.11 slim for smaller size
# slim = نسخه سبک بدون ابزارهای اضافه
FROM python:3.11-slim

# Set working directory inside container
# همه دستورات بعدی در این پوشه اجرا میشن
WORKDIR /app

# Install system dependencies
# gcc, g++ = compiler های C که بعضی کتابخانه های Python بهشون نیاز دارن
# rm -rf /var/lib/apt/lists/* = حذف cache نصب برای کوچیکتر شدن image
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first — for better Docker layer caching
# اگه requirements.txt تغییر نکرده، Docker از cache استفاده میکنه
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir = cache pip رو ذخیره نکن (image کوچیکتر میشه)
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary Python source files
# فقط فایل های لازم کپی میشن — نه PDF، نه chroma_db، نه venv
COPY app.py .
COPY config.py .
COPY ingest.py .
COPY rag.py .

# Expose Streamlit port
# اعلام میکنه container از پورت 8501 استفاده میکنه
EXPOSE 8501

# Health check — بررسی سلامت container
# هر 30 ثانیه چک میکنه برنامه زنده است یا نه
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit when container starts
# --server.port=8501 = پورت 8501 استفاده کن
# --server.address=0.0.0.0 = از همه آدرس ها قابل دسترس باشه
# --server.headless=true = مرورگر خودکار باز نشه
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]