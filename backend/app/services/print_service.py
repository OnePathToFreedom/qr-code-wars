from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
import io
import os

from app.services.qrcode_service import QRCodeService

class PrintService:
    # A4 размер в пикселях при 300 DPI
    A4_WIDTH = 2480  # 210 мм
    A4_HEIGHT = 3508  # 297 мм
    
    # Отступы
    MARGIN = 100
    
    @staticmethod
    def create_a4_sheet_with_qrcodes(urls: List[str], labels: List[str]) -> bytes:
        """
        Создает PDF документ A4 с QR-кодами, организованными в сетку 3x3
        """
        # Создаем лист A4 с белым фоном
        sheet = Image.new('RGB', (PrintService.A4_WIDTH, PrintService.A4_HEIGHT), 'white')
        draw = ImageDraw.Draw(sheet)
        
        # Рассчитываем размеры QR-кода
        qr_per_row = 3
        qr_rows = 3
        
        available_width = PrintService.A4_WIDTH - 2 * PrintService.MARGIN
        available_height = PrintService.A4_HEIGHT - 2 * PrintService.MARGIN
        
        qr_width = available_width // qr_per_row
        qr_height = available_height // qr_rows
        
        # Размер QR-кода с учетом необходимых отступов
        qr_size = min(qr_width, qr_height) - 100
        
        # Загружаем шрифт
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except IOError:
            font = ImageFont.load_default()
        
        # Размещаем QR-коды
        for i, (url, label) in enumerate(zip(urls, labels)):
            if i >= qr_per_row * qr_rows:
                break
                
            row = i // qr_per_row
            col = i % qr_per_row
            
            # Вычисляем положение QR-кода на листе
            x = PrintService.MARGIN + col * qr_width + (qr_width - qr_size) // 2
            y = PrintService.MARGIN + row * qr_height + (qr_height - qr_size) // 2
            
            # Генерируем QR-код
            qr_bytes = QRCodeService.generate_qr_code(url, size=10)
            qr_img = Image.open(io.BytesIO(qr_bytes))
            
            # Изменяем размер QR-кода если нужно
            if qr_img.width != qr_size:
                qr_img = qr_img.resize((qr_size, qr_size))
            
            # Размещаем QR-код на листе
            sheet.paste(qr_img, (x, y))
            
            # Добавляем текст под QR-кодом
            text_width = draw.textlength(label, font=font)
            text_x = x + (qr_size - text_width) // 2
            text_y = y + qr_size + 20
            draw.text((text_x, text_y), label, fill="black", font=font)
        
        # Сохраняем лист в байтовый поток в формате PDF
        buffer = io.BytesIO()
        sheet.save(buffer, format="PDF")
        
        return buffer.getvalue()
    
    @staticmethod
    def generate_printable_qrcodes(phrases, base_url: str = None) -> bytes:
        """
        Создает PDF документ с QR-кодами для всех фраз
        """
        urls = []
        labels = []
        
        for phrase in phrases:
            url = QRCodeService.generate_phrase_url(phrase.hash_url, base_url)
            urls.append(url)
            labels.append(f"QR Code #{phrase.id}")
            
        return PrintService.create_a4_sheet_with_qrcodes(urls, labels) 