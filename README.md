# DevMind :  Second Brain for Developers

An AI-powered knowledge base that extracts and embeds text/code from various file types (PDFs, images, DOCX, source code) into a vector database using Sentence Transformers and ChromaDB. Built to help developers search and recall snippets, functions, and notes from their local files.

---

## Features

### Multi-file Support
- Parses `.py`, `.js`, `.ts`, `.html`, `.css`, `.json`, `.yaml`, `.md` and more.
- Automatically detects file type via extension.

### File Text Extraction
- **PDF Extraction** using PyMuPDF (`fitz`)
- **Image Text Extraction** using Tesseract OCR
- **DOCX Parsing** with `python-docx`

### AI Embeddings
- Converts extracted content into semantic vectors using `sentence-transformers`.

### Code Understanding
- Parses Python files to extract:
  - Function names
  - Docstrings
  - Full source code blocks

### Testing Support
- Will include unit tests for:
  - Text extraction accuracy
  - Embedding similarity
  - Function parsing

### Refactoring Assistant (Planned)
- Refactor and rewrite old code based on AI feedback.
- Code explanation and suggestions.

### ChromaDB Storage
- Stores vectorized data using ChromaDB with metadata:
  - Source path
  - Function name
  - Code/doc chunk