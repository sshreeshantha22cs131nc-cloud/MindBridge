"""

Flow:
1. User uploads a PDF/TXT document
2. We split it into chunks (small pieces)
3. We convert chunks to vectors (embeddings)
4. When user asks a question, we convert question to vector too
5. We find the most similar chunks using cosine similarity
6. We give those chunks to the LLM as context
"""

import numpy as np
import PyPDF2
import io
from models.embeddings import embed_texts, embed_query
from config.config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_RESULTS

MIN_SIMILARITY_THRESHOLD = 0.2


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts all text from a PDF file.

    Parameters:
    - file_bytes: Raw bytes of the PDF file

    Returns:
    - Extracted text as a single string
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        full_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        return full_text.strip()

    except Exception as e:
        print(f"[ERROR] Failed to extract PDF text: {e}")
        return ""


def extract_text_from_txt(file_bytes: bytes) -> str:
    """
    Extracts text from a plain .txt file.
    """
    try:
        return file_bytes.decode("utf-8", errors="ignore").strip()
    except Exception as e:
        print(f"[ERROR] Failed to read TXT file: {e}")
        return ""


def split_into_chunks(text: str) -> list:
    """
    Splits a long text into overlapping chunks.
    Overlap ensures we don't lose context at chunk boundaries.

    Example with CHUNK_SIZE=20, CHUNK_OVERLAP=5:
    Text: "Hello world this is a test of chunking logic here"
    Chunk 1: "Hello world this is a"
    Chunk 2: "is a test of chunking"   ← overlaps with chunk 1
    Chunk 3: "chunking logic here"

    Parameters:
    - text: Full document text

    Returns:
    - List of text chunk strings
    """
    try:
        chunks = []
        start = 0
        while start < len(text):
            end = start + CHUNK_SIZE
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += CHUNK_SIZE - CHUNK_OVERLAP  # Move forward with overlap

        return chunks

    except Exception as e:
        print(f"[ERROR] Failed to split text into chunks: {e}")
        return []


def build_vector_store(chunks: list) -> dict:
    """
    Converts chunks into embeddings and stores them.
    This is our simple in-memory "vector database".

    Parameters:
    - chunks: List of text chunks

    Returns:
    - Dictionary with 'chunks' and 'embeddings'
    """
    try:
        if not chunks:
            return {"chunks": [], "embeddings": []}

        print(f"[INFO] Building vector store for {len(chunks)} chunks...")
        embeddings = embed_texts(chunks)

        return {
            "chunks": chunks,
            "embeddings": embeddings
        }

    except Exception as e:
        print(f"[ERROR] Failed to build vector store: {e}")
        return {"chunks": [], "embeddings": []}


def retrieve_relevant_chunks(query: str, vector_store: dict) -> str:

    try:
        if not vector_store or not vector_store.get("chunks"):
            return ""

        chunks = vector_store["chunks"]
        embeddings = vector_store["embeddings"]

        if len(embeddings) == 0:
            return ""

        query_vector = embed_query(query)
        if query_vector is None:
            return ""

        embeddings_2d = np.array(embeddings)
        
        similarities = np.dot(embeddings_2d, query_vector)

        n_chunks = len(similarities)
        k = TOP_K_RESULTS if TOP_K_RESULTS < n_chunks else n_chunks

        if k == 0:
            return ""

        if k < n_chunks:
            top_indices = np.argpartition(similarities, -k)[-k:]
        else:
            top_indices = np.arange(n_chunks)

        unique_scores = {}
        for idx in top_indices:
            score = similarities[idx]
            if score > MIN_SIMILARITY_THRESHOLD:
                unique_scores[score] = idx

        if not unique_scores:
            return ""

        sorted_scores = sorted(unique_scores.keys(), reverse=True)[:TOP_K_RESULTS]
        top_chunks = [chunks[unique_scores[s]] for s in sorted_scores]

        return "\n\n".join(top_chunks)

    except Exception as e:
        print(f"[ERROR] Failed to retrieve chunks: {e}")
        return ""


def process_uploaded_file(uploaded_file) -> dict:
    """
    Full pipeline: takes an uploaded Streamlit file object,
    extracts text, chunks it, and builds a vector store.

    Parameters:
    - uploaded_file: Streamlit UploadedFile object

    Returns:
    - vector_store dict ready for retrieval
    """
    try:
        file_bytes = uploaded_file.read()
        filename = uploaded_file.name.lower()

        # Extract text based on file type
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_bytes)
        elif filename.endswith(".txt"):
            text = extract_text_from_txt(file_bytes)
        else:
            return {"chunks": [], "embeddings": [], "error": "Unsupported file type. Please upload PDF or TXT."}

        if not text:
            return {"chunks": [], "embeddings": [], "error": "Could not extract text from file."}

        # Split and embed
        chunks = split_into_chunks(text)
        vector_store = build_vector_store(chunks)
        vector_store["filename"] = uploaded_file.name
        vector_store["total_chunks"] = len(chunks)

        print(f"[INFO] Processed '{uploaded_file.name}': {len(chunks)} chunks created.")
        return vector_store

    except Exception as e:
        print(f"[ERROR] Failed to process uploaded file: {e}")
        return {"chunks": [], "embeddings": [], "error": str(e)}
