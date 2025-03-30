from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import Settings
from src.database.models import Base

class DatabaseConnection:
    def __init__(self):
        self.engine = create_engine(Settings.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()