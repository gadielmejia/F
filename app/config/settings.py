import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # SECRET_KEY: lee env; en dev usa valor por defecto si falta.
    _secret = os.getenv("SECRET_KEY") or "dev-secret-key-change-me"
    SECRET_KEY = _secret

    # DATABASE_URL tiene prioridad sobre la construcción tradicional MYSQL_*.
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        # Si el usuario provee DATABASE_URL (puede ser mysql+pymysql://... o sqlite://...)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Fallback a los componentes MYSQL_* (útil en producción con MySQL)
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{os.getenv('MYSQL_USER')}:"
            f"{os.getenv('MYSQL_PASSWORD')}@"
            f"{os.getenv('MYSQL_HOST')}:"
            f"{int(os.getenv('MYSQL_PORT', '3306'))}/"
            f"{os.getenv('MYSQL_DATABASE')}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLOUDINARY_URL = os.getenv("CLOUDINARY_URL", "").strip()
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "").strip()
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "").strip()
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "").strip()
    CLOUDINARY_UPLOAD_FOLDER = os.getenv(
        "CLOUDINARY_UPLOAD_FOLDER", "RentStyle/prendas"
    ).strip()

    if CLOUDINARY_URL and not (
        CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET
    ):
        from urllib.parse import urlparse

        parsed = urlparse(CLOUDINARY_URL)
        if parsed.scheme == "cloudinary":
            CLOUDINARY_API_KEY = CLOUDINARY_API_KEY or parsed.username
            CLOUDINARY_API_SECRET = CLOUDINARY_API_SECRET or parsed.password
            CLOUDINARY_CLOUD_NAME = CLOUDINARY_CLOUD_NAME or parsed.hostname
