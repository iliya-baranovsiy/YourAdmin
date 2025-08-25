from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from configurations.loadEnv import DATA_BASE_URL
from datetime import datetime

Base = declarative_base()


class GameNews(Base):
    __tablename__ = "games_news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    text = Column(String)
    picture = Column(String)
    adding_Date = Column(Date)


class BaseWork:
    def __init__(self):
        self.__engine = create_engine(DATA_BASE_URL)
        self._Session = sessionmaker(bind=self.__engine)
        # self._session = self.__Session()

    def _create_bases(self):
        Base.metadata.create_all(self.__engine)


class GameNewsWork(BaseWork):
    def insert_data(self, title, text, picture):
        with self._Session() as session:
            new_entry = GameNews(title=title, text=text, picture=picture, adding_Date=datetime.today().date())
            session.add(new_entry)
            session.commit()
            session.close()


games_news_db = GameNewsWork()
