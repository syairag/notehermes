import os
from dotenv import load_dotenv

load_dotenv()

class AIConfig:
    """Configuration for the AI Service and Model Routing."""
    
    # Base Provider Settings
    API_KEY = os.getenv("DASHSCOPE_API_KEY")
    BASE_URL = os.getenv("DASHSCOPE_BASE_URL", "https://coding.dashscope.aliyuncs.com/v1")
    
    # Team Model Assignments (The "All-Star" Roster)
    MODELS = {
        "backend": os.getenv("MODEL_BACKEND", "qwen3-coder-next"),       # Agent #1: Code Specialist
        "frontend": os.getenv("MODEL_FRONTEND", "qwen3.6-plus"),         # Agent #2: Visual + Thinking
        "ai_nlp": os.getenv("MODEL_AI_NLP", "glm-5"),                    # Agent #3: Reasoning Specialist
        "qa": os.getenv("MODEL_QA", "MiniMax-M2.5"),                     # Agent #4: Fast + Thinking
        "architect": os.getenv("MODEL_ARCHITECT", "kimi-k2.5"),          # Tony: Vision + Deep Thinking
    }
    
    # Fallback Model
    DEFAULT_MODEL = os.getenv("MODEL_DEFAULT", "qwen-plus")

    @classmethod
    def get_model(cls, role: str = "default") -> str:
        """Get the specific model for a given role."""
        return cls.MODELS.get(role, cls.DEFAULT_MODEL)
