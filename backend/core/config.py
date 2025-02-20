<<<<<<< HEAD
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pydantic import Field, FilePath, BaseModel
from pathlib import Path

load_dotenv()

BASE_PATH = Path(__file__).resolve().parent.parent

class JWTKeysSettings(BaseModel):
    private_key_path: FilePath = Field(default=BASE_PATH / "core/jwt_key/private.key", description="Путь к приватному ключу")
    public_key_path: FilePath = Field(default=BASE_PATH / "core/jwt_key/public.key", description="Путь к публичному ключу")

    def get_private_key(self) -> str:
        if not self.private_key_path.exists():
            raise FileNotFoundError(f"Приватный ключ формата .key не был получен: {self.private_key_path}")
        return self.private_key_path.read_text(encoding='utf-8').strip()

    def get_public_key(self) -> str:
        if not self.public_key_path.exists():
            raise FileNotFoundError(f"Публичный ключ формата .key не был получен: {self.public_key_path}")
        return self.public_key_path.read_text(encoding='utf-8').strip()

class Settings(BaseSettings):
    url_database: str = Field(alias='DATABASE_URL')
    jwt_keys: JWTKeysSettings = Field(default_factory=JWTKeysSettings)

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='forbid'
    )

=======
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pydantic import Field, FilePath, BaseModel
from pathlib import Path

load_dotenv()

BASE_PATH = Path(__file__).resolve().parent.parent

class JWTKeysSettings(BaseModel):
    private_key_path: FilePath = Field(default=BASE_PATH / "core/jwt_key/private.key", description="Путь к приватному ключу")
    public_key_path: FilePath = Field(default=BASE_PATH / "core/jwt_key/public.key", description="Путь к публичному ключу")

    def get_private_key(self) -> str:
        if not self.private_key_path.exists():
            raise FileNotFoundError(f"Приватный ключ формата .key не был получен: {self.private_key_path}")
        return self.private_key_path.read_text(encoding='utf-8').strip()

    def get_public_key(self) -> str:
        if not self.public_key_path.exists():
            raise FileNotFoundError(f"Публичный ключ формата .key не был получен: {self.public_key_path}")
        return self.public_key_path.read_text(encoding='utf-8').strip()

class Settings(BaseSettings):
    url_database: str = Field(alias='DATABASE_URL')
    jwt_keys: JWTKeysSettings = Field(default_factory=JWTKeysSettings)

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='forbid'
    )

>>>>>>> d8a3317a0a70d13af2213931a89ea36727542756
settings = Settings()