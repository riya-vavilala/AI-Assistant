from pathlib import Path

from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

DOCUMENTS_DIR = Path("documents")
CHROMA_DIR = "chroma_db"


def load_pdf(file_path):
    """Extract text from a PDF."""
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def main():

    all_text = []

    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files.")

    for pdf_file in pdf_files:

        print(f"Processing: {pdf_file.name}")

        text = load_pdf(pdf_file)

        if text.strip():
            all_text.append(text)

    combined_text = "\n".join(all_text)

    print("Text extraction completed.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(combined_text)

    print(f"Created {len(chunks)} chunks.")

    # Local embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Creating embeddings...")

    Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    print("Vector database created successfully!")


if __name__ == "__main__":
    main()