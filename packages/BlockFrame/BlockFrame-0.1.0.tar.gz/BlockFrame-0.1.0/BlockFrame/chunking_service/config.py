import json, xml, tomllib
import pathlib


class Config:
    def __init__(self, file_path):
        self.file_path = file_path
        self.option_dict = {
            "json": "from_json",
            "py": "from_pyfile",
            "xml": "from_xml",
            "toml": "from_toml",
        }

        self.execute_config_extraction = self.option_dict[str(file_path).split(".")[1]]
        self.config_id = (getattr(self, self.execute_config_extraction))()

    def from_json(self):
        json_data = json.loads(open(self.file_path, "rb").read())
        return json_data

    def from_pyfile(self):
        ...

    def from_xml(self):
        ...

    def from_toml(self):
        ...
