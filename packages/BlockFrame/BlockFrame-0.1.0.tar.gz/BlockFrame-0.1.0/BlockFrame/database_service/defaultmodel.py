from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Relationship

from BlockFrame.database_service.initalisation import DatabaseInterface


class DefaultChunkModel(DatabaseInterface().Base):
    __tablename__ = "ChunkModel-default"
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_uuid = Column(String)
    file_name = Column(String)
    size = Column(Integer)
    original_file_hash = Column(String)
    split_length = Column(Integer)
    linking_id = Column(String)
    hashes = Relationship("ChunkHashes", backref="default_chunk")


class ChunkHashes(DatabaseInterface().Base):
    __tablename__ = "ChunkModel-hashes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chunk_hash = Column(String)
    linking_id = Column(String, ForeignKey("ChunkModel-default.id"))
    chunk_length = Column(Integer)
    chunk_size = Column(Integer)  # kilobytes
