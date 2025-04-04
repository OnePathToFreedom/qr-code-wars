from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Optional
import hashlib
import random

from app.db.base import get_db
from app.models.phrase import Phrase
from app.services.qrcode_service import QRCodeService
from app.services.print_service import PrintService

router = APIRouter(prefix="/phrases", tags=["phrases"])

@router.get("/")
def get_phrases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список всех фраз
    """
    phrases = db.query(Phrase).offset(skip).limit(limit).all()
    return phrases

@router.get("/{hash_url}")
def get_phrase_by_hash(hash_url: str, db: Session = Depends(get_db)):
    """
    Получить фразу по хешу URL
    """
    phrase = db.query(Phrase).filter(Phrase.hash_url == hash_url).first()
    if not phrase:
        raise HTTPException(status_code=404, detail="Фраза не найдена")
    return phrase

@router.post("/")
def create_phrase(text: str, location_name: Optional[str] = None, 
                 location_x: Optional[int] = None, location_y: Optional[int] = None,
                 db: Session = Depends(get_db)):
    """
    Создать новую фразу
    """
    # Генерируем временный ID для создания хеша
    temp_id = random.randint(10000, 999999)
    hash_url = QRCodeService.generate_hash_url(temp_id)
    
    # Создаем запись в базе данных
    phrase = Phrase(
        text=text,
        hash_url=hash_url,
        location_name=location_name,
        location_x=location_x,
        location_y=location_y
    )
    
    db.add(phrase)
    db.commit()
    db.refresh(phrase)
    
    # Обновляем хеш с использованием реального ID
    phrase.hash_url = QRCodeService.generate_hash_url(phrase.id)
    db.commit()
    
    return phrase

@router.get("/{phrase_id}/qrcode")
def get_phrase_qrcode(phrase_id: int, db: Session = Depends(get_db)):
    """
    Получить QR-код для фразы
    """
    phrase = db.query(Phrase).filter(Phrase.id == phrase_id).first()
    if not phrase:
        raise HTTPException(status_code=404, detail="Фраза не найдена")
    
    url = QRCodeService.generate_phrase_url(phrase.hash_url)
    qr_code = QRCodeService.generate_qr_code(url)
    
    return Response(content=qr_code, media_type="image/png")

@router.get("/print/all")
def print_all_phrases(db: Session = Depends(get_db)):
    """
    Получить PDF документ со всеми QR-кодами для печати
    """
    phrases = db.query(Phrase).all()
    pdf_data = PrintService.generate_printable_qrcodes(phrases)
    
    return Response(content=pdf_data, media_type="application/pdf") 