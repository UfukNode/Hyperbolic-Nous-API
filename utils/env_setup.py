import os
from dotenv import load_dotenv

def load_environment():
    load_dotenv()
    
    config = {
        "HYPERBOLIC_API_KEY": os.getenv("HYPERBOLIC_API_KEY"),
        "PORT": int(os.getenv("PORT", 8000)),
        "DEBUG": os.getenv("DEBUG", "False").lower() == "true",
        "ENVIRONMENT": os.getenv("ENVIRONMENT", "production"),
        "HYPERBOLIC_BASE_URL": os.getenv("HYPERBOLIC_BASE_URL", "https://api.hyperbolic.xyz/v1"),
        "DEFAULT_MODEL": os.getenv("DEFAULT_MODEL", "nous-hermes-2-mixtral-8x7b-dpo")
    }
    
    return config
