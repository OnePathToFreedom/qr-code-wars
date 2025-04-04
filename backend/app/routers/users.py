from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import hashlib
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.db.base import get_db
from app.models.user import User
from app.models.scan import Scan
from app.config import settings

router = APIRouter(prefix="/users", tags=["users"])

# Настройка безопасности
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Недействительные учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register")
def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя
    """
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже зарегистрирован")
    
    db_email = db.query(User).filter(User.email == email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже зарегистрирован")
    
    hashed_password = get_password_hash(password)
    user = User(username=username, email=email, hashed_password=hashed_password)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Создаем JWT токен для пользователя
    access_token = create_access_token(
        data={"sub": user.username}
    )
    
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Вход пользователя и получение JWT токена
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.username}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Получить информацию о текущем пользователе
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }

@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    """
    Получить лидерборд пользователей по количеству собранных фраз
    """
    leaders = db.query(
        User.id,
        User.username,
        db.func.count(Scan.id).label("scans_count")
    ).join(Scan).group_by(User.id).order_by(db.func.count(Scan.id).desc()).limit(10).all()
    
    return [
        {"id": id, "username": username, "scans_count": scans_count}
        for id, username, scans_count in leaders
    ]

@router.post("/scan/{phrase_hash}")
def scan_qr_code(
    phrase_hash: str, 
    user_agent: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Отметить QR-код как отсканированный текущим пользователем
    """
    # Находим фразу по хешу
    from app.models.phrase import Phrase
    phrase = db.query(Phrase).filter(Phrase.hash_url == phrase_hash).first()
    if not phrase:
        raise HTTPException(status_code=404, detail="QR-код не найден")
    
    # Проверяем, сканировал ли пользователь уже этот QR-код
    existing_scan = db.query(Scan).filter(
        Scan.user_id == current_user.id,
        Scan.phrase_id == phrase.id
    ).first()
    
    if existing_scan:
        return {"message": "Вы уже отсканировали этот QR-код"}
    
    # Создаем запись о сканировании
    scan = Scan(
        user_id=current_user.id,
        phrase_id=phrase.id,
        user_agent=user_agent
    )
    
    db.add(scan)
    db.commit()
    
    return {"message": "QR-код успешно добавлен"} 