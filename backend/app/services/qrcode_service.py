import qrcode
import hashlib
from io import BytesIO
from typing import Optional
import base64

from app.config import settings

class QRCodeService:
    @staticmethod
    def generate_hash_url(phrase_id: int) -> str:
        """
        Генерирует защищенный хеш для URL QR-кода
        """
        data = f"{phrase_id}{settings.QR_SECRET_SALT}"
        hash_obj = hashlib.sha256(data.encode())
        return hash_obj.hexdigest()[:12]
    
    @staticmethod
    def generate_qr_code(url: str, size: int = 10) -> bytes:
        """
        Генерирует QR-код для указанного URL
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Сохраняем изображение в байтовый поток
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        
        return buffer.getvalue()
    
    @staticmethod
    def generate_qr_base64(url: str, size: int = 10) -> str:
        """
        Генерирует QR-код и возвращает его в формате base64
        """
        qr_bytes = QRCodeService.generate_qr_code(url, size)
        return base64.b64encode(qr_bytes).decode('utf-8')
    
    @staticmethod
    def generate_phrase_url(hash_url: str, base_url: Optional[str] = None) -> str:
        """
        Создает полный URL для QR-кода
        """
        if not base_url:
            base_url = "http://localhost:3000"  # Для разработки
        
        return f"{base_url}/phrase/{hash_url}" 