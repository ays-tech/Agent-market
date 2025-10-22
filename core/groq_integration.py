"""
GroqCloud Integration - Handle model selection and API configuration
"""
from typing import Optional, Dict, List
import os


# Available Groq models
AVAILABLE_MODELS = {
    "llama-3.3-70b-versatile": {
        "name": "Llama 3.3 70B",
        "description": "Most capable Llama model, versatile for various tasks",
        "provider": "Meta"
    },
    "llama-3.1-70b-versatile": {
        "name": "Llama 3.1 70B",
        "description": "Previous generation Llama, still very capable",
        "provider": "Meta"
    },
    "llama-3.1-8b-instant": {
        "name": "Llama 3.1 8B Instant",
        "description": "Fast and efficient smaller model",
        "provider": "Meta"
    },
    "mixtral-8x7b-32768": {
        "name": "Mixtral 8x7B",
        "description": "Mixture of experts model with 32k context",
        "provider": "Mistral"
    },
    "gemma2-9b-it": {
        "name": "Gemma 2 9B",
        "description": "Google's efficient instruction-tuned model",
        "provider": "Google"
    }
}


def get_available_models() -> Dict[str, Dict]:
    """Get list of available models"""
    return AVAILABLE_MODELS


def get_model_names() -> List[str]:
    """Get list of model names"""
    return list(AVAILABLE_MODELS.keys())


def validate_model(model_name: str) -> bool:
    """Check if model name is valid"""
    return model_name in AVAILABLE_MODELS


def get_model_info(model_name: str) -> Optional[Dict]:
    """Get information about a specific model"""
    return AVAILABLE_MODELS.get(model_name)


class GroqConfig:
    """Configuration for Groq API"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.model = model if validate_model(model) else "llama-3.3-70b-versatile"
    
    def is_configured(self) -> bool:
        """Check if API key is configured"""
        return bool(self.api_key)
    
    def get_api_key_status(self) -> str:
        """Get status message about API key"""
        if self.is_configured():
            return f"✅ API Key configured (ends with ...{self.api_key[-4:]})"
        else:
            return "⚠️ No API key found. Set GROQ_API_KEY environment variable or enter in sidebar."


# Singleton config instance
_config = None


def get_config() -> GroqConfig:
    """Get or create config instance"""
    global _config
    if _config is None:
        _config = GroqConfig()
    return _config


def set_api_key(api_key: str):
    """Set API key"""
    global _config
    if _config is None:
        _config = GroqConfig(api_key=api_key)
    else:
        _config.api_key = api_key
    
    # Also set environment variable for Agno
    os.environ["GROQ_API_KEY"] = api_key


def set_model(model: str):
    """Set default model"""
    global _config
    if _config is None:
        _config = GroqConfig(model=model)
    else:
        _config.model = model

