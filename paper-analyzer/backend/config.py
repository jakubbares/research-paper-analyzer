"""
Configuration management using pydantic-settings
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # LLM Provider
    llm_provider: str = "bedrock"  # bedrock, deepseek, openai, etc.
    
    # DeepSeek
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"
    deepseek_model_temperature: float = 0.1
    deepseek_max_tokens: int = 4096
    
    # AWS Configuration
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    
    # AWS Bedrock
    bedrock_model_id: str = "deepseek-ai.deepseek-v3"
    bedrock_model_temperature: float = 0.1
    bedrock_max_tokens: int = 4096
    
    # Application
    debug: bool = True
    log_level: str = "INFO"
    api_port: int = 8000
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:3001"
    
    # Data Directories
    upload_dir: str = "data/uploads"
    extracted_dir: str = "data/extracted"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def origins_list(self) -> List[str]:
        """Parse allowed origins into list"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


# Global settings instance
settings = Settings()

