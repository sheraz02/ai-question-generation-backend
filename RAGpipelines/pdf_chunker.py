"""
pdf_chunker.py

Create overlapping text chunks from a large PDF using LangChain.

Usage:
    python pdf_chunker.py /path/to/large.pdf

Requirements:
    pip install langchain pypdf python-dotenv tqdm

Notes:
 - Uses PyPDFLoader (from langchain.document_loaders) to page-load a PDF.
 - Uses RecursiveCharacterTextSplitter by default; you can switch to CharacterTextSplitter.
 - Yields chunks (generator) so you don't need to keep everything in memory.
"""


import uuid
import json
import os
from typing import Generator, Dict, Any, Iterable, Optional, List
from tqdm import tqdm

from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

def make_text_splitter(
        chunk_size: int = 1000, chunk_overlap: int = 200, splitter_type: str = "recursive",
):
    """
    Create and return a configured text splitter.

    splitter_type: "recursive" or "simple"
    """
    if splitter_type == "simple":
        return CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    # default to recursive (better at respecting structure)
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

def pdf_chunk_generator(
        pdf_path: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        splitter_type: str = "recursive",
        pages: Optional[Iterable[int]] = None,
) -> Generator[Dict[str, Any], None, None]:
    """
    Generator that yields text chunks from a PDF.

    Yields dict:
      {
        "chunk_id": str,           # unique id (uuid4)
        "text": str,               # chunk text
        "page": int,               # 1-indexed page number
        "page_chunk_index": int,   # index of chunk within that page (0-based)
        "global_chunk_index": int, # sequential index across document (0-based)
        "meta": dict               # other metadata (e.g., source file)
      }

    Arguments:
      pdf_path: path to the PDF file
      chunk_size: approx characters per chunk
      chunk_overlap: overlap between chunks
      splitter_type: "recursive" or "simple"
      pages: optional iterable of 0-based page indices to include (e.g., [0,2,3]).
             If None, iterates over all pages.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found : {pdf_path}")
    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    text_splitter = make_text_splitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, splitter_type=splitter_type)

    global_idx = 0

    for page_idx, doc in enumerate(tqdm(documents, desc="Pages", unit="page")):
        if pages is not None and page_idx not in pages:
            continue

        page_text = doc.page_content or ""
        if not page_text.strip():
            continue

        chunks = text_splitter.split_text(page_text)
        for page_chunk_index, chunk_text in enumerate(chunks):
            chunk = {
                "chunk_id": str(uuid.uuid4()),
                "text": chunk_text,
                "page": page_idx + 1,
                "page_chunk_index": page_chunk_index,
                "global_chunk_index": global_idx,
                "meta": {
                    "source": os.path.abspath(path=pdf_path),
                    **(doc.metadata or {}),
                },
            }
            yield chunk
            global_idx += 1

def save_chunks_to_jsonl(chunks: Iterable[Dict[str, Any]], output_path: str):
    """
    Save chunk dicts to a newline-delimited JSON file (jsonl).
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        for c in chunks:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Chunk a large PDF into overlapping text pieces (generator).")
    parser.add_argument("pdf", help="Path to the PDF file.")
    parser.add_argument(
        "--chunk-size", "-s", type=int, default=1000, help="Approximate number of characters per chunk."
    )
    parser.add_argument(
        "--overlap", "-o", type=int, default=200, help="Number of overlapping characters between consecutive chunks."
    )
    parser.add_argument(
        "--splitter", choices=["recursive", "simple"], default="recursive", help="Which text splitter to use."
    )
    parser.add_argument("--jsonl", "-j", help="If provided, save chunks to this JSONL path.")
    parser.add_argument("--start-page", type=int, default=None, help="1-indexed start page to include.")
    parser.add_argument("--end-page", type=int, default=None, help="1-indexed end page to include (inclusive).")
    args = parser.parse_args()

    # pages selection conversion to 0-based indices if start/end provided
    pages_arg = None
    if args.start_page is not None or args.end_page is not None:
        # convert to 0-based inclusive range
        # If only start provided, go to end of document; we will filter inside generator so safe.
        start = (args.start_page - 1) if args.start_page is not None else 0
        end = (args.end_page - 1) if args.end_page is not None else None
        # build pages set lazily by scanning doc length; simpler: create range with a large upper bound and generator will skip missing pages.
        # But better: load documents once to get length here
        loader_for_len = PyPDFLoader(args.pdf)
        docs_for_len = loader_for_len.load()
        if end is None:
            end = len(docs_for_len) - 1
        pages_arg = range(max(0, start), min(len(docs_for_len) - 1, end) + 1)

    gen = pdf_chunk_generator(
        args.pdf,
        chunk_size=args.chunk_size,
        chunk_overlap=args.overlap,
        splitter_type=args.splitter,
        pages=pages_arg,
    )

    if args.jsonl:
        print(f"Saving chunks to {args.jsonl} ...")
        save_chunks_to_jsonl(gen, args.jsonl)
        print("Saved.")
    else:
        # just iterate and print summary
        count = 0
        for chunk in gen:
            # show a short preview
            preview = chunk["text"][:120].replace("\n", " ").strip()
            print(f"[G#{chunk['global_chunk_index']}] page {chunk['page']} chunk {chunk['page_chunk_index']}: {preview}...")
            count += 1
        print(f"Total chunks: {count}")