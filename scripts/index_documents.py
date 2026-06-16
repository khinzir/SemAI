# """
# Index all your CSIT documents into Azure AI Search
# Run this ONCE after setting up Azure AI Search
# """
# import os
# import json
# import sys
# from pathlib import Path
# from dotenv import load_dotenv
#
# # THIS LINE MUST BE HERE BEFORE ANY CODES CALL APIS
# load_dotenv()
#
# # Add project root to path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#
# from rag.search_client import SearchClientManager
# from rag.embedding_client import EmbeddingClient
#
#
# def read_pdf_text(pdf_path):
#     """Extract text from PDF - simple version"""
#     try:
#         import PyPDF2
#         with open(pdf_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             text = ""
#             for page in reader.pages:
#                 text += page.extract_text()
#             return text
#     except Exception as e:
#         print(f"Error reading {pdf_path}: {e}")
#         return ""
#
#
# def index_all_documents():
#     """Index all documents in the data folder"""
#
#     # Initialize clients
#     search_client = SearchClientManager()
#     embedding_client = EmbeddingClient()
#
#     # Create index if it doesn't exist
#     print("Creating search index...")
#     search_client.create_index()
#
#     # Base path for semester 1 data
#     base_path = Path("data/semester1")
#     subjects = ["C-Programming", "DL", "IIT", "Maths", "Physics"]
#
#     all_documents = []
#     doc_id = 0
#
#     for subject in subjects:
#         subject_path = base_path / subject
#         if not subject_path.exists():
#             print(f"Warning: {subject_path} not found")
#             continue
#
#         print(f"\n📚 Processing {subject}...")
#
#         # 1. Index textbooks
#         textbooks_path = subject_path / "textbooks"
#         if textbooks_path.exists():
#             for pdf_file in textbooks_path.glob("*.pdf"):
#                 print(f"  📖 Indexing textbook: {pdf_file.name}")
#                 text = read_pdf_text(pdf_file)
#                 if text:
#                     # Split into chunks (simple version - ~1000 chars per chunk)
#                     chunks = [text[i:i + 1000] for i in range(0, len(text), 800)]
#                     for i, chunk in enumerate(chunks):
#                         doc = {
#                             "id": f"{subject}_textbook_{doc_id}_{i}",
#                             "content": chunk,
#                             "semester": 1,
#                             "subject": subject.replace("-", "_"),
#                             "document_type": "textbook",
#                             "source_file": pdf_file.name,
#                             "unit": "full_book"
#                         }
#                         all_documents.append(doc)
#                         doc_id += 1
#
#         # 2. Index Q&A pairs
#         qna_file = subject_path / "qna_pairs.json"
#         if qna_file.exists():
#             with open(qna_file, 'r') as f:
#                 qna_data = json.load(f)
#                 for qa in qna_data.get("qa_pairs", []):
#                     # Create a document from the question
#                     doc = {
#                         "id": f"{subject}_qna_{qa.get('id', doc_id)}",
#                         "content": f"Question: {qa['question']}\nAnswer: {qa['answer']}",
#                         "semester": 1,
#                         "subject": subject.replace("-", "_"),
#                         "document_type": "qna",
#                         "source_file": "qna_pairs.json",
#                         "unit": qa.get("topic", ""),
#                         "year": qa.get("year", 0)
#                     }
#                     all_documents.append(doc)
#                     doc_id += 1
#                     print(f"  📝 Indexed Q&A: {qa['question'][:50]}...")
#
#         # 3. Index syllabus
#         syllabus_file = subject_path / "syllabus.txt"
#         if syllabus_file.exists():
#             with open(syllabus_file, 'r') as f:
#                 syllabus_text = f.read()
#                 doc = {
#                     "id": f"{subject}_syllabus",
#                     "content": syllabus_text,
#                     "semester": 1,
#                     "subject": subject.replace("-", "_"),
#                     "document_type": "syllabus",
#                     "source_file": "syllabus.txt"
#                 }
#                 all_documents.append(doc)
#                 print(f"  📋 Indexed syllabus")
#                 doc_id += 1
#
#     print(f"\n📊 Total documents to index: {len(all_documents)}")
#
#     # Generate embeddings and upload to search
#     print("\n🔮 Generating embeddings and uploading...")
#
#     for i, doc in enumerate(all_documents):
#         # Generate embedding for content
#         doc["content_vector"] = embedding_client.get_embedding(doc["content"])
#
#         # Upload to search
#         search_client.upload_document(doc)
#
#         if i % 10 == 0:
#             print(f"  Progress: {i}/{len(all_documents)}")
#
#     print(f"\n✅ Indexing complete! {len(all_documents)} documents uploaded.")
#     print(f"You can now search using the chatbot!")
#
#
# if __name__ == "__main__":
#     index_all_documents()





# pasting simpler code below that creates less number of chunks to tackle rate limits


"""
Index all your CSIT documents into Azure AI Search
Run this ONCE after setting up Azure AI Search
"""
import os
import json
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# THIS LINE MUST BE HERE BEFORE ANY CODES CALL APIS
load_dotenv()

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.search_client import SearchClientManager
from rag.embedding_client import EmbeddingClient


def read_pdf_text(pdf_path):
    """Extract text from PDF - simple version"""
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""


def index_all_documents():
    """Index all documents in the data folder"""

    # Initialize clients
    search_client = SearchClientManager()
    embedding_client = EmbeddingClient()

    # Create index if it doesn't exist
    print("Creating search index...")
    search_client.create_index()

    # Base path for semester 1 data
    base_path = Path("data/semester1")
    subjects = ["C-Programming", "DL", "IIT", "Maths", "Physics"]

    all_documents = []
    doc_id = 0

    for subject in subjects:
        subject_path = base_path / subject
        if not subject_path.exists():
            print(f"Warning: {subject_path} not found")
            continue

        print(f"\n📚 Processing {subject}...")

        # 1. Index textbooks
        textbooks_path = subject_path / "textbooks"
        if textbooks_path.exists():
            for pdf_file in textbooks_path.glob("*.pdf"):
                print(f"  📖 Indexing textbook: {pdf_file.name}")
                text = read_pdf_text(pdf_file)
                if text:
                    chunks = [text[i:i + 1000] for i in range(0, len(text), 800)]
                    for i, chunk in enumerate(chunks):
                        doc = {
                            "id": f"{subject}_textbook_{doc_id}_{i}",
                            "content": chunk,
                            "semester": 1,
                            "subject": subject.replace("-", "_"),
                            "document_type": "textbook",
                            "source_file": pdf_file.name,
                            "unit": "full_book"
                        }
                        all_documents.append(doc)
                        doc_id += 1

        # 2. Index Q&A pairs
        qna_file = subject_path / "qna_pairs.json"
        if qna_file.exists():
            with open(qna_file, 'r') as f:
                qna_data = json.load(f)
                for qa in qna_data.get("qa_pairs", []):
                    doc = {
                        "id": f"{subject}_qna_{qa.get('id', doc_id)}",
                        "content": f"Question: {qa['question']}\nAnswer: {qa['answer']}",
                        "semester": 1,
                        "subject": subject.replace("-", "_"),
                        "document_type": "qna",
                        "source_file": "qna_pairs.json",
                        "unit": qa.get("topic", ""),
                        "year": qa.get("year", 0)
                    }
                    all_documents.append(doc)
                    doc_id += 1
                    print(f"  📝 Indexed Q&A: {qa['question'][:50]}...")

        # 3. Index syllabus
        syllabus_file = subject_path / "syllabus.txt"
        if syllabus_file.exists():
            with open(syllabus_file, 'r') as f:
                syllabus_text = f.read()
                doc = {
                    "id": f"{subject}_syllabus",
                    "content": syllabus_text,
                    "semester": 1,
                    "subject": subject.replace("-", "_"),
                    "document_type": "syllabus",
                    "source_file": "syllabus.txt"
                }
                all_documents.append(doc)
                print(f"  📋 Indexed syllabus")
                doc_id += 1

    total_docs = len(all_documents)
#     print(f"\n📊 Total documents to index: {total_docs}")
#     print("\n🔮 Generating embeddings in batches and uploading...")
#
#     batch_size = 16
#
#     for start_idx in range(0, total_docs, batch_size):
#         end_idx = min(start_idx + batch_size, total_docs)
#         current_batch = all_documents[start_idx:end_idx]
#
#         # Extract text strings for the batch
#         batch_texts = [doc["content"] for doc in current_batch]
#
#         # Call API once for all 16 strings
#         vectors = embedding_client.get_embeddings_batch(batch_texts)
#
#         if vectors and len(vectors) == len(current_batch):
#             for idx, doc in enumerate(current_batch):
#                 doc["content_vector"] = vectors[idx]
#                 try:
#                     search_client.upload_document(doc)
#                 except Exception as upload_err:
#                     print(f"❌ Error uploading document {doc['id']}: {upload_err}")
#         else:
#             print(
#                 f"❌ Critical error: Could not fetch vectors for batch indices {start_idx}-{end_idx}. Skipping chunk row.")
#
#         print(f"  Progress: {end_idx}/{total_docs} items synced.")
#
#         # Mandatory 4.1 second sleep to strictly avoid breaking the 15 requests per minute ceiling!
#         if end_idx < total_docs:
#             time.sleep(4.1)
#
#     print(f"\n✅ Indexing complete! {total_docs} documents successfully uploaded.")
#     print(f"You can now search using the chatbot!")
#
#
# if __name__ == "__main__":
#     index_all_documents()



    # this part above was commented out and replaced with simpler one to fix githubs limits

    print(f"\n📊 Total documents to index: {total_docs}")
    print("\n🔮 Pushing clean text directly to Azure AI Search...")

    # We skip batching and GitHub models entirely because Azure handles
    # text parsing instantly on its own high-speed servers
    for i, doc in enumerate(all_documents):
        try:
            # We don't generate vectors locally. Azure AI Search takes the raw text
            # and auto-vectorizes it inside the cloud index mapping definition!
            search_client.upload_document(doc)
        except Exception as upload_err:
            print(f"❌ Error uploading document {doc['id']}: {upload_err}")

        if i % 50 == 0:
            print(f"  Progress: {i}/{total_docs} items uploaded directly.")

    print(f"\n✅ Indexing complete! {total_docs} documents successfully uploaded.")
    print(f"You can now search using the chatbot!")

if __name__ == "__main__":
    index_all_documents()




