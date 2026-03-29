import os
import hashlib
import gc
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from config import (
    EMBEDDING_MODEL, CHROMA_PATH, COLLECTION_NAME,
    CHUNK_SIZE, CHUNK_OVERLAP, BATCH_SIZE, MAX_FILE_SIZE_MB
)

# Cache مدل Embedding
_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        print("🔄 لود مدل Embedding...")
        _embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        print("✅ مدل لود شد!")
    return _embedding_model

def get_vectorstore(embedding_model=None):
    if embedding_model is None:
        embedding_model = get_embedding_model()
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=CHROMA_PATH
    )

def get_file_hash(file_path):
    """Hash یکتا از محتوای فایل"""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_existing_hashes():
    """همه hash های موجود در ChromaDB"""
    try:
        vs = get_vectorstore()
        results = vs.get()
        hashes = set()
        if results and "metadatas" in results:
            for meta in results["metadatas"]:
                if meta and "file_hash" in meta:
                    hashes.add(meta["file_hash"])
        return hashes
    except:
        return set()

def get_existing_sources():
    """همه اسم فایل‌های موجود"""
    try:
        vs = get_vectorstore()
        results = vs.get()
        sources = set()
        if results and "metadatas" in results:
            for meta in results["metadatas"]:
                if meta and "source" in meta:
                    source = meta["source"].replace("\\", "/").split("/")[-1]
                    if source.startswith("temp_"):
                        source = source[5:]
                    sources.add(source)
        return sources
    except:
        return set()

def get_database_stats():
    """آمار کامل بانک اطلاعاتی"""
    try:
        vs = get_vectorstore()
        results = vs.get()
        
        if not results or not results.get("ids"):
            return {"total_chunks": 0, "total_docs": 0, "docs": []}
        
        total_chunks = len(results["ids"])
        docs_chunks = {}
        
        for meta in results.get("metadatas", []):
            if meta and "source" in meta:
                source = meta["source"].replace("\\", "/").split("/")[-1]
                if source.startswith("temp_"):
                    source = source[5:]
                docs_chunks[source] = docs_chunks.get(source, 0) + 1
        
        return {
            "total_chunks": total_chunks,
            "total_docs": len(docs_chunks),
            "docs": [{"name": k, "chunks": v} for k, v in docs_chunks.items()]
        }
    except Exception as e:
        print(f"⚠️ خطا در آمار: {e}")
        return {"total_chunks": 0, "total_docs": 0, "docs": []}

def check_file_size(file_path):
    """بررسی حجم فایل"""
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return False, size_mb
    return True, size_mb

def load_document(file_path):
    """بارگذاری فایل PDF یا TXT"""
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError("فقط PDF یا TXT قبول میشه!")
    
    documents = loader.load()
    print(f"✅ {len(documents)} صفحه خونده شد")
    return documents

def split_documents(documents, file_hash, file_name):
    """تقسیم به chunk با metadata کامل"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    
    for chunk in chunks:
        chunk.metadata["file_hash"] = file_hash
        chunk.metadata["file_name"] = file_name
    
    print(f"✅ {len(chunks)} chunk ساخته شد")
    return chunks

def save_to_chroma_optimized(chunks, progress_callback=None):
    """
    ذخیره بهینه برای ۱۰۰+ فایل
    - پردازش batch به batch
    - آزاد کردن حافظه بعد از هر batch
    - جلوگیری از timeout
    """
    print("⏳ شروع ذخیره‌سازی بهینه...")
    embedding_model = get_embedding_model()
    vectorstore = get_vectorstore(embedding_model)
    
    total = len(chunks)
    saved = 0
    
    for i in range(0, total, BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]
        
        try:
            vectorstore.add_documents(batch)
            saved += len(batch)
            
            if progress_callback:
                progress = saved / total
                progress_callback(progress, saved, total)
            
            print(f"📦 Batch {i//BATCH_SIZE + 1}: {saved}/{total} chunk ذخیره شد")
            
            # آزاد کردن حافظه بعد از هر batch
            gc.collect()
            
        except Exception as e:
            print(f"❌ خطا در batch {i//BATCH_SIZE + 1}: {e}")
            continue
    
    print(f"✅ {saved}/{total} chunk با موفقیت ذخیره شد!")
    return vectorstore

def delete_document(file_name):
    """حذف یه سند از ChromaDB"""
    try:
        vs = get_vectorstore()
        results = vs.get()
        ids_to_delete = []
        
        if results and "metadatas" in results:
            for idx, meta in enumerate(results["metadatas"]):
                if meta and "source" in meta:
                    source = meta["source"].replace("\\", "/").split("/")[-1]
                    if source.startswith("temp_"):
                        source = source[5:]
                    if source == file_name:
                        ids_to_delete.append(results["ids"][idx])
        
        if ids_to_delete:
            vs.delete(ids=ids_to_delete)
            print(f"✅ {len(ids_to_delete)} chunk از {file_name} حذف شد")
            return len(ids_to_delete)
        return 0
    except Exception as e:
        print(f"❌ خطا در حذف: {e}")
        return 0

def vacuum_database():
    """بهینه‌سازی و فشرده‌سازی بانک"""
    import shutil
    print("🔄 شروع Vacuum...")
    
    try:
        vs = get_vectorstore()
        results = vs.get()
        
        if not results or not results.get("ids"):
            return 0
        
        total_before = len(results["ids"])
        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])
        ids = results.get("ids", [])
        
        # پاک کردن بانک قدیمی
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
        
        # ساخت بانک جدید تمیز
        embedding_model = get_embedding_model()
        new_vs = get_vectorstore(embedding_model)
        
        # اضافه کردن داده‌ها به صورت batch
        for i in range(0, len(documents), BATCH_SIZE):
            batch_docs = documents[i:i+BATCH_SIZE]
            batch_meta = metadatas[i:i+BATCH_SIZE]
            batch_ids = ids[i:i+BATCH_SIZE]
            new_vs._collection.add(
                documents=batch_docs,
                metadatas=batch_meta,
                ids=batch_ids
            )
            gc.collect()
        
        print(f"✅ Vacuum کامل — {len(documents)} chunk")
        return len(documents)
        
    except Exception as e:
        print(f"❌ خطا در Vacuum: {e}")
        return -1

def ingest(file_path, progress_callback=None):
    """تابع اصلی ایندکس با بهینه‌سازی کامل"""
    print(f"\n📄 پردازش: {file_path}")
    print("=" * 50)
    
    # تمیز کردن اسم فایل
    file_name = os.path.basename(file_path)
    if file_name.startswith("temp_"):
        file_name = file_name[5:]
    
    # بررسی حجم فایل
    ok, size_mb = check_file_size(file_path)
    if not ok:
        print(f"❌ فایل خیلی بزرگه: {size_mb:.1f}MB > {MAX_FILE_SIZE_MB}MB")
        return "too_large"
    
    print(f"📊 حجم فایل: {size_mb:.1f}MB")
    
    # بررسی hash
    file_hash = get_file_hash(file_path)
    print(f"🔑 Hash: {file_hash[:8]}...")
    
    existing_hashes = get_existing_hashes()
    if file_hash in existing_hashes:
        return "duplicate_hash"
    
    existing_sources = get_existing_sources()
    if file_name in existing_sources:
        return "duplicate_name"
    
    # پردازش
    documents = load_document(file_path)
    chunks = split_documents(documents, file_hash, file_name)
    save_to_chroma_optimized(chunks, progress_callback)
    
    # آزاد کردن حافظه
    del documents
    del chunks
    gc.collect()
    
    print("=" * 50)
    print("🎉 ایندکس شد!")
    return "success"