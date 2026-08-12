from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)
import os
from config import *
from utils.helper import allowed_file
from utils.data_loader import load_csv, dataset_summary
from utils.data_cleaner import clean_dataset
from utils.data_analysis import (
    numerical_summary,
    correlation_matrix,
    unique_values
)
from utils.visualization import create_visualizations
from ml.preprocessing import preprocess_dataset
from ml.train import train_model
from ml.predict import preprocess_input
from ml.predict import predict
from ai.gemini_client import GeminiClient
from ai.prompt import SYSTEM_PROMPT
from ai.csv_chat import build_csv_context
from ai.dataframe_agent import DataFrameAgent
from rag.pdf_loader import extract_text
from rag.text_splitter import split_text
from rag.embeddings import EmbeddingGenerator
from rag.faiss_index import FAISSIndex
from rag.hybrid_retriever import HybridRetriever
from ai.prompt_templates import get_prompt_template
from ai.memory import ConversationMemory
import markdown



app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CHART_FOLDER"] = CHART_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.secret_key = SECRET_KEY
app.config["PDF_UPLOAD_FOLDER"] = PDF_UPLOAD_FOLDER

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["CHART_FOLDER"], exist_ok=True)
os.makedirs(app.config["REPORT_FOLDER"], exist_ok=True)
os.makedirs("ml/saved_models", exist_ok=True)
os.makedirs(
    app.config["PDF_UPLOAD_FOLDER"],
    exist_ok=True
)
CURRENT_DOCUMENT_TYPE = None
CURRENT_DATAFRAME = None
CURRENT_MEMORY = ConversationMemory()
CURRENT_MODEL = None

CURRENT_SCALER = None

CURRENT_ENCODERS = None

CURRENT_TARGET_ENCODER = None

CURRENT_FEATURES = None

CURRENT_TARGET = None
CURRENT_PDF_TEXT = ""
CURRENT_PDF_CHUNKS = []
CHAT_MESSAGE = None
EMBEDDER = EmbeddingGenerator()


CURRENT_EMBEDDINGS = []
CURRENT_FAISS = None
CURRENT_RETRIEVER = None
AI_CLIENT = GeminiClient()
KNOWLEDGE_BASE = []
CURRENT_DOCUMENTS = []


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    global CURRENT_EMBEDDINGS
    global CURRENT_DATAFRAME
    global CURRENT_PDF_TEXT
    global CURRENT_PDF_CHUNKS

    if "file" not in request.files:
        return "No file uploaded"

    file = request.files["file"]

    if file.filename == "":
        return "No selected file"

    if not allowed_file(file.filename):
        return "Invalid file type"

    # ============================
    # CSV Upload
    # ============================

    if file.filename.lower().endswith(".csv"):

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        df = load_csv(filepath)

        original_rows = len(df)

        df = clean_dataset(df)

        cleaned_rows = len(df)

        CURRENT_DATAFRAME = df

        cleaning_report = {
            "original_rows": original_rows,
            "cleaned_rows": cleaned_rows,
            "duplicates_removed":
                original_rows - cleaned_rows
        }

        summary = dataset_summary(df)

        statistics = numerical_summary(df)

        charts = create_visualizations(
            df,
            app.config["CHART_FOLDER"]
        )

        correlation = correlation_matrix(df)

        unique = unique_values(df)

        preview = df.head(10).to_html(
            classes="table",
            index=False
        )

        correlation_html = correlation.to_html(
            classes="table",
            border=0
        )

        columns = list(df.columns)

        return render_template(
            "dashboard.html",
            preview=preview,
            summary=summary,
            cleaning=cleaning_report,
            statistics=statistics,
            correlation=correlation_html,
            unique=unique,
            charts=charts,
            columns=columns
        )

    # ============================
# PDF Upload
# ============================

    elif file.filename.lower().endswith(".pdf"):

        filepath = os.path.join(
            app.config["PDF_UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        print("=" * 60)
        print("PDF Saved At:", filepath)
        print("=" * 60)

        # -----------------------------------
        # Extract page-wise text
        # -----------------------------------

        pages = extract_text(filepath)

        CURRENT_PDF_TEXT = pages

        full_text = "\n".join(
            page["text"]
            for page in pages
        )

        # -----------------------------------
        # Empty PDF Check
        # -----------------------------------

        if not full_text.strip():

            return """
    This PDF contains no extractable text.

    It may be a scanned/image PDF and requires OCR support.
    """

        # -----------------------------------
        # Detect Document Type
        # -----------------------------------

        from ai.document_classifier import classify_document

        global CURRENT_DOCUMENT_TYPE

        CURRENT_DOCUMENT_TYPE = classify_document(
            full_text
        )

        print(
            "Document Type:",
            CURRENT_DOCUMENT_TYPE
        )

        # -----------------------------------
        # Split into chunks
        # -----------------------------------

        new_chunks = split_text(
            pages,
            chunk_size=500,
            overlap=100
        )

        for chunk in new_chunks:

            chunk["document"] = file.filename

        # Add to Knowledge Base

        CURRENT_PDF_CHUNKS.extend(
            new_chunks
        )

        CURRENT_DOCUMENTS.append(
            file.filename
        )

        print(
            "Total Chunks:",
            len(CURRENT_PDF_CHUNKS)
        )

        # -----------------------------------
        # Embeddings
        # -----------------------------------

        new_embeddings = EMBEDDER.embed_chunks(
            new_chunks
        )

        CURRENT_EMBEDDINGS.extend(
            new_embeddings
        )

        print(
            "Total Embeddings:",
            len(CURRENT_EMBEDDINGS)
        )

        if not new_embeddings:

            return "Embedding generation failed."

        # -----------------------------------
        # Build / Update FAISS
        # -----------------------------------

        global CURRENT_FAISS

        if CURRENT_FAISS is None:

            dimension = len(
                new_embeddings[0]
            )

            CURRENT_FAISS = FAISSIndex(
                dimension
            )

        CURRENT_FAISS.add_vectors(
            new_embeddings
        )

        CURRENT_FAISS.save(
            FAISS_INDEX_FILE
        )

        # -----------------------------------
        # Retriever
        # -----------------------------------

        global CURRENT_RETRIEVER

        CURRENT_RETRIEVER = HybridRetriever(
            EMBEDDER,
            CURRENT_FAISS.index,
            CURRENT_PDF_CHUNKS
        )

        print("Retriever Ready")

        # -----------------------------------
        # Success Message
        # -----------------------------------

        global CHAT_MESSAGE

        CHAT_MESSAGE = f"""
    PDF uploaded successfully.

    Uploaded Documents : {len(CURRENT_DOCUMENTS)}

    {chr(10).join(CURRENT_DOCUMENTS)}

    Pages : {len(CURRENT_PDF_TEXT)}

    Characters : {len(full_text)}

    Total Chunks : {len(CURRENT_PDF_CHUNKS)}

    Total Embeddings : {len(CURRENT_EMBEDDINGS)}

    Document Type : {CURRENT_DOCUMENT_TYPE}

    Knowledge Base Ready ✓
    """

        return redirect(
            url_for("chat")
        )

    return redirect(
        url_for("home")
    )

@app.route("/train", methods=["POST"])
def train():

    global CURRENT_DATAFRAME

    if CURRENT_DATAFRAME is None:
        return "Upload a dataset first."

    # Get form data
    target = request.form["target"]
    model_name = request.form["model"]

    # Detect task
    if CURRENT_DATAFRAME[target].dtype in ["object", "bool", "category"]:
        task = "classification"
    else:
        task = "regression"

    if CURRENT_DATAFRAME[target].isnull().any():
        return "Target column contains missing values."
    

    # Preprocess dataset
    processed = preprocess_dataset(
        CURRENT_DATAFRAME,
        target
    )

    global CURRENT_SCALER
    global CURRENT_ENCODERS
    global CURRENT_TARGET_ENCODER
    global CURRENT_FEATURES
    global CURRENT_TARGET

    CURRENT_SCALER = processed["scaler"]
    CURRENT_ENCODERS = processed["encoders"]
    CURRENT_TARGET_ENCODER = processed["target_encoder"]
    CURRENT_FEATURES = list(
        CURRENT_DATAFRAME.drop(columns=[target]).columns
    )
    CURRENT_TARGET = target

    # -------- PASTE IT HERE --------
    save_path = os.path.join(
        "ml",
        "saved_models",
        f"{model_name.replace(' ', '_').lower()}.pkl"
    )

    # Train model
    result = train_model(
        processed_data=processed,
        model_name=model_name,
        task=task,
        save_path=save_path
    )
    global CURRENT_MODEL
    CURRENT_MODEL = result["model"]

    # Show results
    return render_template(
        "train.html",
        metrics=result["metrics"],
        model_name=model_name,
        task=task
    )

@app.route("/predict", methods=["GET", "POST"])
def prediction():

    global CURRENT_MODEL
    global CURRENT_SCALER
    global CURRENT_ENCODERS
    global CURRENT_TARGET_ENCODER
    global CURRENT_FEATURES

    if CURRENT_MODEL is None:

        return "Train a model first."

    if request.method == "POST":

        input_data = {}

        for feature in CURRENT_FEATURES:

            value = request.form[feature]

            try:
                value = float(value)
            except ValueError:
                pass

            input_data[feature] = value

        processed = preprocess_input(

            input_data,

            CURRENT_SCALER,

            CURRENT_ENCODERS

        )

        result = predict(

            CURRENT_MODEL,

            processed,

            CURRENT_TARGET_ENCODER

        )

        return render_template(

            "predict.html",

            features=CURRENT_FEATURES,

            prediction=result

        )

    return render_template(

        "predict.html",

        features=CURRENT_FEATURES,

        prediction=None

    )

@app.route("/chat", methods=["GET", "POST"])
def chat():

    global CHAT_MESSAGE
    global CURRENT_DATAFRAME
    global CURRENT_RETRIEVER
    global CURRENT_DOCUMENT_TYPE

    answer = CHAT_MESSAGE
    CHAT_MESSAGE = None

    if request.method == "POST":

        question = request.form["question"].strip()

        CURRENT_MEMORY.add_user(question)

        # ==========================================
        # CSV DATAFRAME AGENT
        # ==========================================

        local_answer = None

        if CURRENT_DATAFRAME is not None:

            try:

                agent = DataFrameAgent(
                    CURRENT_DATAFRAME
                )

                local_answer = agent.answer(
                    question
                )

            except Exception:

                local_answer = None

        # ==========================================
        # CSV Answer
        # ==========================================

        if local_answer:

            prompt = f"""
{SYSTEM_PROMPT}

You are an expert data analyst.

Conversation History

{CURRENT_MEMORY.get_history()}

A pandas dataframe agent produced the following answer.

Result

{local_answer}

Rules

- Explain clearly.
- Use Markdown.
- Use bullet points.
- Use tables if useful.
- Do not invent values.
"""

        # ==========================================
        # PDF RAG
        # ==========================================

        else:

            retrieved_chunks = []

            if CURRENT_RETRIEVER is not None:

                retrieved_chunks = CURRENT_RETRIEVER.retrieve(
                    question,
                    top_k=3
                )

            if not retrieved_chunks:

                answer = markdown.markdown(
                    "I could not find this information in the uploaded document."
                )

                return render_template(
                    "chat.html",
                    answer=answer
                )

            # --------------------------------------
            # Build Context
            # --------------------------------------

            context_parts = []

            source_list = []

            for chunk in retrieved_chunks:

                context_parts.append(
                    chunk["text"]
                )

                if chunk["page"] is not None:

                    source_list.append(

                        f"{chunk['document']} • "
                        f"Page {chunk['page']} "
                        f"(Chunk {chunk['chunk_id']})"

                    )

            pdf_context = "\n\n".join(
                context_parts
            )

            source_text = "\n".join(

                f"- {source}"

                for source in sorted(
                    set(source_list)
                )
            )

            format_rules = """
            - Use Markdown.
            - Use headings.
            - Use bullet points for lists.
            - Use numbered steps for procedures.
            - Use tables for comparisons.
            - Keep answers clean and structured.
            """

            prompt = f"""
{SYSTEM_PROMPT}
You are an intelligent multi-document AI assistant.

The retrieved context may come from one or more uploaded PDFs.

Use ONLY the retrieved context.

If multiple documents contain relevant information,
combine the information while preserving the source.

Never invent information.

{CURRENT_MEMORY.get_history()}

Retrieved Context

{pdf_context}

Available Sources

{source_text}

User Question

{question}

Instructions

1. Answer ONLY from the retrieved context.

2. Never use outside knowledge.

3. Never rewrite the entire document.

4. Never summarize unrelated sections.

5. Maximum 120 words unless the user asks for details.

6. Use clean Markdown.

7. If the answer is unavailable reply EXACTLY:

I could not find this information in the uploaded document.

Formatting

{format_rules}
At the end ALWAYS include

### Sources

List every document and page used.

Example

### Sources

- Resume.pdf • Page 2
- Research.pdf • Page 5

Do not invent sources.

Never invent page numbers.
"""

        # ==========================================
        # Gemini
        # ==========================================

        try:

            response = AI_CLIENT.ask(
                prompt
            )

            CURRENT_MEMORY.add_ai(response)

            answer = markdown.markdown(
                response,
                extensions=[
                    "tables",
                    "fenced_code"
                ]
            )

        except Exception as e:

            answer = markdown.markdown(
                f"**Gemini Error:** {str(e)}"
            )

    return render_template(
        "chat.html",
        answer=answer
    )

@app.route("/chunks")
def chunks():

    global CURRENT_PDF_CHUNKS

    if not CURRENT_PDF_CHUNKS:
        return "No chunks available. Upload a PDF first."

    return "<hr>".join(CURRENT_PDF_CHUNKS)

@app.route("/retrieve")
def retrieve_test():

    global CURRENT_RETRIEVER

    if CURRENT_RETRIEVER is None:

        return "Upload PDF first."

    chunks = CURRENT_RETRIEVER.retrieve(

        "Summarize this document",

        top_k=2

    )

    return "<hr>".join(chunks)

if __name__ == "__main__":
    app.run(debug=True)






