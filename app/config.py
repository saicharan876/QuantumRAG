import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
    QDRANT_URL=os.getenv("QDRANT_URL")
    QDRANT_API_KEY=os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION="rag"
    GROQ_API_KEY=os.getenv("GROQ_API_KEY")
    GROQ_FALLBACK_API_KEY=os.getenv("GROQ_FALLBACK_API_KEY")
    GROQ_MODEL = "llama-3.3-70b-versatile"


settings = Settings()




    
