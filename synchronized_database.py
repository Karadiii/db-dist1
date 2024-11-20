from persistent_database import PersistentDatabase
import threading
import multiprocessing


class SynchronizedDatabase(PersistentDatabase):
    def __init__(self, file_path, mode="threads"):
        super().__init__(file_path)
        self.mode = mode
        self.lock = threading.Lock() if mode == "threads" else multiprocessing.Lock()
        self.reader_count = 0
        self.reader_count_lock = threading.Lock() if mode == "threads" else multiprocessing.Lock()
        self.reader_semaphore = threading.Semaphore(10) if mode == "threads" else multiprocessing.Semaphore(10)

    def acquire_read(self):
        with self.reader_count_lock:
            self.reader_semaphore.acquire()
            self.reader_count += 1
            if self.reader_count == 1:
                self.lock.acquire()

    def release_read(self):
        with self.reader_count_lock:
            self.reader_count -= 1
            if self.reader_count == 0:
                self.lock.release()
            self.reader_semaphore.release()

    def acquire_write(self):
        self.lock.acquire()

    def release_write(self):
        self.lock.release()

    def set_value(self, key, val):
        self.acquire_write()
        try:
            super().set_value(key, val)
        finally:
            self.release_write()

    def get_value(self, key):
        self.acquire_read()
        try:
            return super().get_value(key)
        finally:
            self.release_read()

    def delete_value(self, key):
        self.acquire_write()
        try:
            super().delete_value(key)
        finally:
            self.release_write()
