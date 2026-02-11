from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from typing import List, Dict
from langchain_community.docstore.document import Document
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# PDF_PATH = "files/my_document.pdf"            # <-- change this to your PDF file path
PERSIST_DIR = "chroma_db"                     # where Chroma will persist data
COLLECTION_NAME = "pdf_fixed_chunks"
CHUNK_SIZE = 800      # characters (fixed-size)
CHUNK_OVERLAP = 150   # characters overlap (helps context continuity)
# EMBEDDING_MODEL = "text-embedding-3-small"  # for OpenAIEmbeddings (change if needed)
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # set this in env

def load_pdf_documents(pdf_path: str) -> List[Document]:
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    return pages
c = load_pdf_documents('pdf-files/postgis.pdf')
for d in c:
    print(d.page_content)
print()

def fixed_chunk_documents(docs: List[Document], chunk_size: int, chunk_overlap: int, separator: str = "\n") -> List[Document]:
    splitter = CharacterTextSplitter(
        separator=separator,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    out_docs: List[Document] = []

    for doc in docs:
        chunks = splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            md = dict(doc.metadata) if doc.metadata else {}
            md.update({
                "chunk_index": i,
                "chunk_size": len(chunk)
            })
            out_docs.append(Document(page_content=chunk, metadata=md))
    return out_docs

def create_chroma_from_documents(documents: List[Document], persist_dir: str, collection_name: str):

    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    vector = embeddings.embed_query("hello sheraz!")
    
    vectorDB = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=persist_dir
    )
    vectorDB.persist()
    return vectorDB

def query_chroma(vectorDB: Chroma, query: str, k: int = 5):
    results = vectorDB.similarity_search(query, k=k)
    return results

def main():
    pdf_path = 'pdf-files/postgis.pdf'


    print(f"Loading PDF: {pdf_path}")
    raw_docs = load_pdf_documents(str(pdf_path))
    print(f"Loaded {len(raw_docs)} page documents from PDF")

    print(f"Applying fixed-size chunking: chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}")
    chunked_docs = fixed_chunk_documents(raw_docs, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    print(f"Produced {len(chunked_docs)} chunks")
    print(chunked_docs)

    # Optional: add a source metadata (useful in retrieval)
    # for d in chunked_docs:
    #     if "source" not in d.metadata:
    #         d.metadata["source"] = str(pdf_path)

    # print("Creating Chroma DB and embedding the chunks (this may take time / cost tokens)...")
    # vectordb = create_chroma_from_documents(chunked_docs, persist_dir=PERSIST_DIR, collection_name=COLLECTION_NAME)
    # print("Chroma DB persisted to:", PERSIST_DIR)

    # # Quick example query
    # q = "Explain the OSI model layers"  # example; replace with something relevant
    # print(f"\nRunning similarity search for: {q}")
    # hits = query_chroma(vectordb, q, k=5)
    # for i, h in enumerate(hits):
    #     print(f"\n--- Hit {i+1} ---")
    #     print("Score: N/A (langchain returns documents; use vectordb.get_relevant_documents for scores depending on impl)")
    #     print("Metadata:", h.metadata)
    #     print("Content preview:", h.page_content[:400].replace("\n", " "))



# if __name__ == "__main__":
#     main()