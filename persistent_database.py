from database import Database
import pickle


class PersistentDatabase(Database):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self._load_from_file()

    def _load_from_file(self):
        """Loads the database from the file if it exists."""
        try:
            with open(self.file_path, "rb") as file:
                self._data = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self._data = {}  # Initialize an empty database if the file is missing or empty.

    def _save_to_file(self):
        """Saves the current state of the database to the file."""
        with open(self.file_path, "wb") as file:
            pickle.dump(self._data, file)

    def set_value(self, key, val):
        super().set_value(key, val)
        self._save_to_file()

    def delete_value(self, key):
        super().delete_value(key)
        self._save_to_file()
