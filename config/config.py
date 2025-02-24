from langchain_openai import OpenAIEmbeddings

## API
OPENAI_API_KEY = "T"
QDRANT_SERVER = ""
QDRANT_API_KEY = ""
collection_name=""

# Path
pdf_path = "../data/upload/triethoc.pdf"

# Variable
_k = 10
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
