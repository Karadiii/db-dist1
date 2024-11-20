class Database:
    def __init__(self):
        self._data = {}

    def set_value(self, key, val):
        """Sets the value for a given key."""
        self._data[key] = val

    def get_value(self, key):
        """Gets the value for a given key. Raises KeyError if not found."""
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found in database.")
        return self._data[key]

    def delete_value(self, key):
        """Deletes a given key from the database. Raises KeyError if not found."""
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found in database.")
        del self._data[key]

    def __repr__(self):
        return f"Database({self._data})"
