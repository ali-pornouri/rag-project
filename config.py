import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# مدل Embedding چندزبانه
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# تنظیمات ChromaDB
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "rag_docs"

# تنظیمات Groq
GROQ_MODEL = "llama-3.3-70b-versatile"
MAX_TOKENS = 1000
TEMPERATURE = 0.2

# تنظیمات تقسیم متن — بهینه برای کتاب‌های بزرگ
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# تنظیمات جستجو
TOP_K = 5
FETCH_K = 10
MMR_LAMBDA = 0.85
SCORE_THRESHOLD = 0.0
SHOW_SCORES = True

# تنظیمات چندزبانه
ENABLE_TRANSLATION = True

# ✅ تنظیمات بهینه برای ۱۰۰+ فایل
BATCH_SIZE = 50          # تعداد chunk در هر batch
MAX_BATCH_BYTES = 5000   # حداکثر bytes در هر batch
MAX_FILE_SIZE_MB = 50    # حداکثر حجم هر فایل