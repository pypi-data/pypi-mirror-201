from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import create_engine
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    database_url = Field(
        env="DATABASE_URL",
        default="postgresql://postgresUser:postgresPW@localhost:5432/postgresDB",
    )

    def get_engine(self):
        try:
            assert self.database_url
            return create_engine(self.database_url)
        except AssertionError as error:
            print(error)
        return None

    @staticmethod
    def get_session(db_engine):
        return scoped_session(
            sessionmaker(autoflush=False, bind=db_engine)
        )


settings = Settings()
engine = settings.get_engine()
db_session = Settings.get_session(engine)


def get_session():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
