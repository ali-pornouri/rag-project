import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from groq import Groq
from config import (
    EMBEDDING_MODEL,
    CHROMA_PATH,
    COLLECTION_NAME,
    GROQ_MODEL,
    GROQ_API_KEY,
    MAX_TOKENS,
    TEMPERATURE,
    TOP_K
)

def load_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=CHROMA_PATH
    )
    print("✅ پایگاه داده لود شد")
    return vectorstore

def search_documents(vectorstore, query, k=TOP_K):
    results = vectorstore.similarity_search_with_score(query, k=k)
    context_parts = []
    sources = []
    seen = set()
    
    for doc, score in results:
        context_parts.append(doc.page_content)
        source = doc.metadata.get("source", "نامشخص")
        source = source.replace("\\", "/").split("/")[-1]
        if source.startswith("temp_"):
            source = source[5:]
        page = doc.metadata.get("page", "نامشخص")
        key = f"{source}-{page}"
        if key not in seen:
            seen.add(key)
            sources.append({
                "file": source,
                "page": page,
                "score": round(score, 3)
            })
    
    context = "\n\n".join(context_parts)
    print(f"✅ {len(results)} بخش مرتبط پیدا شد")
    return context, sources

def ask_groq(context, question):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"""بر اساس اطلاعات زیر به سوال جواب بده.
جواب کامل و مفید بده. اگه اطلاعات نبود بگو: "این اطلاعات در اسناد من نیست."

اطلاعات:
{context}

سوال: {question}

جواب:"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )
    return response.choices[0].message.content

def ask(question):
    print(f"\n❓ سوال: {question}")
    print("=" * 50)
    
    vectorstore = load_vectorstore()
    context, sources = search_documents(vectorstore, question)
    answer = ask_groq(context, question)
    
    source_text = "\n\n---\n📚 **منابع:**\n"
    for s in sources:
        if s["page"] != "نامشخص":
            source_text += f"- 📖 **{s['file']}** — صفحه {int(s['page']) + 1}\n"
        else:
            source_text += f"- 📖 **{s['file']}**\n"
    
    full_answer = answer + source_text
    print(f"\n💬 جواب: {answer}")
    print("=" * 50)
    return full_answer