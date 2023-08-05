from sqlalchemy import Column, Integer, String
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


class DatabaseInterface:
    Base = declarative_base()
    db_engine = create_engine("sqlite:///block_frame.db")
    sync_session = sessionmaker(db_engine, class_=sessionmaker, expire_on_commit=False)

    def custom_uri(self: str):
        async_engine = create_engine(self)


class BlockFrameDatabaseInit(DatabaseInterface):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.class_model = kwargs.get("class_model")
        if self.class_model is None:
            from defaultmodel import DefaultChunkModel

            self.db_model = DefaultChunkModel
        else:
            self.db_model = self.class_model

    def create_table(self, db_model):
        with self.db_engine.begin() as conn:
            DatabaseInterface.sync_session(bind=conn)  # <-- change this line
            db_model.metadata.create_all(conn)

    def get_db(self):
        session = self.sync_session()
        try:
            return session
        finally:
            session.close_all()


class BlockFrameModelInstance(DatabaseInterface):
    def __new__(cls):
        instance = super().__new__(cls)
        return instance.Base
