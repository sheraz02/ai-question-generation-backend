from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader



def characterSplitter(text: str, chunk_size: int, chunk_overlap: int, separater = " "):

    text = """
    Artificial Intelligence (AI) is transforming industries.
    It automates tasks, enhances efficiency, and creates new possibilities.
    """

    splitter = CharacterTextSplitter(
        chunk_size = 40,
        chunk_overlap = 10,
        separator = " "
    )

    chunks = splitter.split_text(text=text)

    for i, chunk in enumerate(chunks):
        print(f"------ Chunk {i} ------")
        print(chunk)

