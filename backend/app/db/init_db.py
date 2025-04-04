from sqlalchemy.orm import Session

from app.models.user import User
from app.models.phrase import Phrase
from app.models.scan import Scan
from app.services.qrcode_service import QRCodeService

# Тестовые мотивационные фразы на немецком
test_phrases = [
    "Der Weg ist das Ziel.",  # Путь — это цель
    "Übung macht den Meister.",  # Практика делает мастера
    "Alles hat ein Ende, nur die Wurst hat zwei.",  # Всё имеет конец, только у колбасы их два
    "Wer nicht wagt, der nicht gewinnt.",  # Кто не рискует, тот не выигрывает
    "Morgenstund hat Gold im Mund.",  # Утро вечера мудренее
    "Das Leben ist kein Ponyhof.",  # Жизнь — не прогулка на пони
    "Erst denken, dann handeln.",  # Сначала думай, потом делай
    "Ende gut, alles gut.",  # Всё хорошо, что хорошо кончается
    "Zeit ist Geld.",  # Время — деньги
    "Der frühe Vogel fängt den Wurm.",  # Ранняя птичка ловит червячка
]

def init_db(db: Session) -> None:
    """
    Инициализирует базу данных тестовыми данными
    """
    # Проверяем, есть ли уже фразы в базе
    phrase_count = db.query(Phrase).count()
    if phrase_count == 0:
        # Добавляем тестовые фразы
        for text in test_phrases:
            phrase = Phrase(text=text)
            db.add(phrase)
            db.commit()
            db.refresh(phrase)
            
            # Генерируем хеш URL для каждой фразы
            phrase.hash_url = QRCodeService.generate_hash_url(phrase.id)
            db.commit()
    
    # Проверяем наличие тестового пользователя
    test_user = db.query(User).filter(User.username == "testuser").first()
    if not test_user:
        from app.routers.users import get_password_hash
        hashed_password = get_password_hash("testpassword")
        test_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=hashed_password
        )
        db.add(test_user)
        db.commit()
    
    print(f"База данных инициализирована с {len(test_phrases)} фразами и тестовым пользователем.") 