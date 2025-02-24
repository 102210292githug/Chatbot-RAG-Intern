from langchain_openai import OpenAIEmbeddings

## API
OPENAI_API_KEY = "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"
QDRANT_SERVER = "http://35.94.42.185:6333"
QDRANT_API_KEY = "MEKONGAI-QDRANT-PRIVATE-API-KEY"
collection_name="duck_chatbotRAG_pdf"

# Path
pdf_path = "../data/upload/triethoc.pdf"

# Variable
_k = 10
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")