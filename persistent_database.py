"""
Author: Ido Karadi
Project name: DB Distributed
Description: Part of the DB Distributed program.
This file includes the PersistentDatabase class.
Date: 26/11/24
"""


from database import Database
import pickle


class PersistentDatabase(Database):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self._load_from_file()

    def _load_from_file(self):
        try:
            with open(self.file_path, "rb") as file:
                self._data = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self._data = {}

    def _save_to_file(self):
        with open(self.file_path, "wb") as file:
            pickle.dump(self._data, file)

    def set_value(self, key, val):
        super().set_value(key, val)
        self._save_to_file()

    def delete_value(self, key):
        super().delete_value(key)
        self._save_to_file()
