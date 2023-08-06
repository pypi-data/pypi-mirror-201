from typing import Optional
from pathlib import Path
from pydantic import Extra, BaseModel


class Config(BaseModel, extra=Extra.ignore):
    api_key: str = None
    model_name: str = "gpt-3.5-turbo"
    temperature:float = 0.5
    history_save_path: Path = Path("data/ChatHistory").absolute()
    openai_proxy: str = None
    openai_api_base: str = None
    history_max: int = 10
    admin: list[str] = None
