# app/core/config.py
# from pydantic import BaseSettings


class Settings:
    # Database URL
    DATABASE_URL: str = "sqlite:///./app.db"

    # Superuser info (for initial seeding)
    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "changeme"

    # Other optional settings
    DEBUG: bool = True
    APP_NAME: str = "My FastAPI App"

    # CORS
    all_cors_origins = "*"

    API_V1_STR = "/v1"

    class Config:
        # This tells Pydantic to load environment variables from a .env file
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a single instance to import everywhere
settings = Settings()
