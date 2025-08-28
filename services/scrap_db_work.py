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


class ItNews(Base):
    __tablename__ = "it_news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    text = Column(String)
    picture = Column(String)
    adding_Date = Column(Date)


class CryptoNews(Base):
    __tablename__ = "crypto_news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    text = Column(String)
    picture = Column(String)
    adding_Date = Column(Date)


class ScienceNews(Base):
    __tablename__ = "science_news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    text = Column(String)
    picture = Column(String)
    adding_Date = Column(Date)


class CultureNews(Base):
    __tablename__ = "culture_news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    text = Column(String)
    picture = Column(String)
    adding_Date = Column(Date)


class SportNews(Base):
    __tablename__ = "sport_news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    text = Column(String)
    picture = Column(String)
    adding_Date = Column(Date)


class BaseWork:
    def __init__(self):
        self.__engine = create_engine(DATA_BASE_URL)
        self._Session = sessionmaker(bind=self.__engine)

    def _create_bases(self):
        Base.metadata.create_all(self.__engine)


class GameNewsWork(BaseWork):
    def insert_data(self, title, text, picture):
        with self._Session() as session:
            new_entry = GameNews(title=title, text=text, picture=picture, adding_Date=datetime.today().date())
            session.add(new_entry)
            session.commit()
            session.close()

    def get_title(self):
        with self._Session() as session:
            data = session.query(GameNews.title)
            return [i[0] for i in data]


class ItNewsWork(BaseWork):
    def insert_data(self, title, text, picture):
        with self._Session() as session:
            new_entry = ItNews(title=title, text=text, picture=picture, adding_Date=datetime.today().date())
            session.add(new_entry)
            session.commit()
            session.close()

    def get_title(self):
        with self._Session() as session:
            data = session.query(ItNews.title)
            return [i[0] for i in data]


class CryptoNewsWork(BaseWork):
    def insert_data(self, title, text, picture):
        with self._Session() as session:
            new_entry = CryptoNews(title=title, text=text, picture=picture, adding_Date=datetime.today().date())
            session.add(new_entry)
            session.commit()
            session.close()

    def get_title(self):
        with self._Session() as session:
            data = session.query(CryptoNews.title)
            return [i[0] for i in data]


class ScienceNewsWork(BaseWork):
    def insert_data(self, title, text, picture):
        with self._Session() as session:
            new_entry = ScienceNews(title=title, text=text, picture=picture, adding_Date=datetime.today().date())
            session.add(new_entry)
            session.commit()
            session.close()

    def get_title(self):
        with self._Session() as session:
            data = session.query(ScienceNews.title)
            return [i[0] for i in data]


class CultureNewsWork(BaseWork):
    def insert_data(self, title, text, picture):
        with self._Session() as session:
            new_entry = CultureNews(title=title, text=text, picture=picture, adding_Date=datetime.today().date())
            session.add(new_entry)
            session.commit()
            session.close()

    def get_title(self):
        with self._Session() as session:
            data = session.query(CultureNews.title)
            return [i[0] for i in data]


class SportNewsWork(BaseWork):
    def insert_data(self, title, text, picture):
        with self._Session() as session:
            new_entry = SportNews(title=title, text=text, picture=picture, adding_Date=datetime.today().date())
            session.add(new_entry)
            session.commit()
            session.close()

    def get_title(self):
        with self._Session() as session:
            data = session.query(SportNews.title)
            return [i[0] for i in data]


games_news_db = GameNewsWork()
it_news_db = ItNewsWork()
crypto_news_db = CryptoNewsWork()
science_news_db = ScienceNewsWork()
culture_news_db = CultureNewsWork()
sport_mews_db = SportNewsWork()
base = BaseWork()
#base._create_bases()
