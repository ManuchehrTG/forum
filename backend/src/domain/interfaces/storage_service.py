from abc import ABC, abstractmethod
from fastapi import UploadFile
from pydantic import BaseModel

class FileInfo(BaseModel):
    """Информация о сохраненном файле"""
    path: str
    size: int
    mime_type: str
    hash: str | None = None

class StorageService(ABC):
    """Порт для работы с хранилищем"""
    
    @abstractmethod
    async def save(self, file: UploadFile, is_temp: bool = True, custom_path: str | None = None) -> str:
        """Сохранить файл и вернуть путь"""
        pass
    
    @abstractmethod
    def delete(self, path: str) -> bool:
        """Удалить файл по пути"""
        pass
    
    @abstractmethod
    def get_url(self, path: str) -> str:
        """Получить публичный URL файла"""
        pass
    
    @abstractmethod
    def move(self, source_path: str, new_path: str) -> None:
        """Переместить"""
        pass