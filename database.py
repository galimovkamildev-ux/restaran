from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Konfiguraciya bazy dannikh PostgreSQL
DATABASE_URL = 'postgresql://postgres:1234@localhost:5432/training'

# Sozdanie dvigatelya bazy dannikh
engine = create_engine(DATABASE_URL, echo=True)

# Sozdanie fabriki sessiy
Session = sessionmaker(bind=engine, autoflush=False)

# Osnovnoy klass dlya modeley
class Base(DeclarativeBase):
    pass

# Poluchenie sessii bazy dannikh
def get_db():
    try:
        db_session = Session()
        yield db_session
    finally:
        db_session.close()
