import chromadb
from chromadb.api.types import EmbeddingFunction
from PyPDF2 import PdfReader
from fastembed import TextEmbedding

# Persistent DB
chroma_client = chromadb.PersistentClient(path="vector_store/chroma")

# FastEmbed model
embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")


# Correct Chroma Embedding Function class
class FastEmbedFunction(EmbeddingFunction):
    def __call__(self, input):
        # input = list[str] of texts
        embeddings = embedding_model.embed(input)
        return [e.tolist() for e in embeddings]  # convert to python list

    def name(self):
        return "fastembed-bge-small-v1.5"


embed_fn = FastEmbedFunction()


# Create or load collection — fully valid now
collection = chroma_client.get_or_create_collection(
    name="got_lore",
    embedding_function=embed_fn,
)


def load_pdf_to_rag(path):
    reader = PdfReader(path)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    chunks = [
        full_text[i : i + 500]
        for i in range(0, len(full_text), 500)
        if full_text[i : i + 500].strip()
    ]

    for idx, chunk in enumerate(chunks):
        collection.add(documents=[chunk], ids=[f"chunk_{idx}"])

    print(f"✓ Loaded {len(chunks)} chunks into vector database.")


def retrieve_lore(query):
    results = collection.query(query_texts=[query], n_results=3)
    docs = results["documents"][0]
    return "\n\n".join(docs)
