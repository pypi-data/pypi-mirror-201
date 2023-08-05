import hashlib
import os
from BlockFrame.chunking_service.config import Config
from BlockFrame.chunking_service.chunking import ChunkHandler
from BlockFrame.database_service.database import BlockFrameDatabase


class BlockFrame:
    def __init__(self, config: str):
        self.config = Config(config)
        self.database = BlockFrameDatabase(db_config=self.config)
        self.chunker = ChunkHandler(db=self.database, config=self.config.config_id)


class Reconstruct:
    def __init__(self, ccif_file) -> None:
        self.ccif_file = ccif_file
        self.file_name = ""
        self.size = 0
        self.original_file_hash = ""
        self.chunk_file_hashes = []
        self.chunk_file_uid = []
        self.primary_uuid = ""

    def parser(self, data):
        return [
            elem.strip("' ")
            for elem in data.strip("[]\n")
            .replace("UUID(", "")
            .replace(")", "")
            .split(",")
        ]

    def parse_ccif_file(self):
        with open(self.ccif_file, "rb") as ccif:
            self.primary_uuid: str = ccif.readline().decode("utf-8")

            self.file_name: str = ccif.readline().decode("utf-8")
            self.size: int = ccif.readline().decode("utf-8")
            self.original_file_hash: str = ccif.readline().decode("utf-8")
            self.chunk_file_hashes: list = ccif.readline().decode("utf-8")
            self.chunk_file_uid: list = ccif.readline().decode("utf-8")

        self.primary_uuid = self.parser(self.primary_uuid)

        self.chunk_file_uid = self.parser(self.chunk_file_uid)
        self.chunk_file_hashes = self.parser(self.chunk_file_hashes)
        self.file_name = self.file_name.strip("\n")
        self.size = str(self.size).strip("\n")
        self.original_file_hash = self.original_file_hash.strip("\n")

    def chunk_files(self) -> list:
        return sorted(
            [
                file
                for file in os.listdir()
                if "_chunk_" in file and self.primary_uuid[0] in file
            ],
            key=lambda file: int(file.split("_")[-1].split(".")[0]),
        )

    def construct_file(self):
        """
        It opens the file that we want to reconstruct, then iterates through the chunk files and writes
        them to the reconstructed file
        """
        with open(f"reconstructed/{self.file_name}", "wb+") as reconstructed_file:
            for chunk in self.chunk_files():
                with open(chunk, "rb") as chunk_file:
                    reconstructed_file.write(chunk_file.read())

    def ensure_integrity(self):
        """
        It reads the file in chunks of 1024 bytes and updates the hash object with each chunk
        :return: The return value is a boolean value.
        """
        _hash = hashlib.sha256()
        with open(f"reconstructed/{self.file_name}", "rb") as file:
            chunk = 0
            while chunk != b"":
                chunk = file.read(1024)
                _hash.update(chunk)

        return _hash.hexdigest() == self.original_file_hash

    def run(self):
        """
        The function runs the parse_ccif_file() function, then the construct_file() function, then the
        ensure_integrity() function
        """
        self.parse_ccif_file()
        self.construct_file()
        if self.ensure_integrity():
            print("File integrity ensured")


def scan_for_ccif_files():
    """
    It returns a generator object that yields the name of each file in the current directory that ends
    with ".ccif"
    """
    for file in os.listdir():
        if file.endswith(".ccif"):
            yield file
