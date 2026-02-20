from abc import ABC, abstractmethod
from fastapi import UploadFile

class FileValidator(ABC):
    @abstractmethod
    async def validate(self, file: UploadFile) -> bool:
        """Проверить файл на соответствие требованиям"""
        pass
