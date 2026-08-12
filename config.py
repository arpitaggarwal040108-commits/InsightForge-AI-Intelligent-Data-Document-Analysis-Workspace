import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
CHART_FOLDER = os.path.join(BASE_DIR, "static", "charts")
REPORT_FOLDER = os.path.join(BASE_DIR, "generated_reports")
ALLOWED_EXTENSIONS = {
    "csv",
    "pdf"
}
SECRET_KEY = "smart_ai_data_explorer"
MAX_CONTENT_LENGTH = 100 * 1024 * 1024

GEMINI_MODEL = "gemini-3.6-flash"
GEMINI_TEMPERATURE = 0.3
GEMINI_MAX_OUTPUT_TOKENS = 2048
PDF_UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads",
    "pdf"
)

# ============================
# RAG SETTINGS
# ============================

EMBEDDING_MODEL = "gemini-embedding-001"

TOP_K = 5

FAISS_INDEX_FOLDER = os.path.join(
    BASE_DIR,
    "rag",
    "indexes"
)

FAISS_INDEX_FILE = os.path.join(
    FAISS_INDEX_FOLDER,
    "document.index"
)