import os
import glob
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
import ast
from docx import Document
import fitz  # PyMuPDF
from PIL import Image
import pytesseract

SUPPORTED_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".md": "markdown"
}
model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_image(file_path):
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def extract_functions_from_python_code(code):
    """
    Parses Python code and extracts functions as separate chunks with:
    - function name
    - docstring (if any)
    - full source code of the function
    Returns a list of dicts: [{ "name": str, "doc": str, "code": str }]
    """
    tree = ast.parse(code)
    funcs = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            start_line = node.lineno - 1  # lineno is 1-indexed
            end_line = node.end_lineno    # inclusive
            lines = code.splitlines()
            func_code = "\n".join(lines[start_line:end_line])
            docstring = ast.get_docstring(node) or ""

            funcs.append({
                "name": node.name,
                "doc": docstring,
                "code": func_code
            })
    return funcs

def load_files(directory="kb"):
    chunks = []
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            ext = file.lower().split('.')[-1]

            if ext == "py":
                # your existing Python function extraction here
                pass
            elif ext == "pdf":
                text = extract_text_from_pdf(path)
            elif ext == "docx":
                text = extract_text_from_docx(path)
            elif ext in ["png", "jpg", "jpeg", "bmp"]:
                text = extract_text_from_image(path)
            else:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()

            chunks.append({
                "source": path,
                "function": "N/A",
                "doc": "",
                "code": text
            })
    return chunks


def get_embeddings(texts):
    return model.encode(texts).tolist()

def store_in_chroma(docs):
    # chroma_client = chromadb.Client()
    chroma_client = chromadb.HttpClient(host="localhost", port=8000)
    try:
        chroma_collection = chroma_client.get_collection(name="second_brain")
    except Exception:
        chroma_collection = chroma_client.create_collection(name="second_brain")

    for idx, doc in enumerate(docs):
        text_to_store = f"Function: {doc['function']}\n\nDocstring:\n{doc['doc']}\n\nCode:\n{doc['code']}"
        chroma_collection.add(
            documents=[text_to_store],
            metadatas=[{"source": doc["source"], "function": doc["function"]}],
            ids=[str(idx)],
        )
    return chroma_collection



